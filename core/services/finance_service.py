import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta
from core.repositories.base_repo import get_connection

def process_credit_card_expense(account_id, date_str, amount, currency, category_id, description, installments, status='Completado', is_recurring=0):
    """
    Process a credit card expense, deducting from available limit and creating installments.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Validate account and get CC info
        cursor.execute("SELECT name, currency FROM accounts WHERE id = ?", (account_id,))
        account = cursor.fetchone()
        if not account:
            raise ValueError("Cuenta no encontrada")

        cursor.execute("SELECT limit_clp, limit_usd, available_clp, available_usd, payment_day FROM credit_cards_info WHERE account_id = ?", (account_id,))
        cc_info = cursor.fetchone()
        if not cc_info:
            raise ValueError("Información de tarjeta de crédito no encontrada para esta cuenta. Asegúrate de haberla configurado correctamente.")
        
        payment_day = cc_info['payment_day']
        if not payment_day:
            payment_day = 5 # Default fallback
            
        # 2. Register transaction
        cursor.execute("""
            INSERT INTO transactions (
                date, type, amount, currency, account_id, category_id, description, status, is_recurring, installments
            ) VALUES (?, 'Egreso', ?, ?, ?, ?, ?, ?, ?, ?)
        """, (date_str, float(amount), currency, account_id, category_id, description, status, int(is_recurring), installments))
        
        # 3. Update available limits and balance (debt increases)
        if currency == 'CLP':
            cursor.execute("""
                UPDATE credit_cards_info 
                SET available_clp = available_clp - ?
                WHERE account_id = ?
            """, (float(amount), account_id))
        elif currency == 'USD':
            cursor.execute("""
                UPDATE credit_cards_info 
                SET available_usd = available_usd - ?
                WHERE account_id = ?
            """, (float(amount), account_id))
            
        # Update balance to reflect total debt (increases for credit card)
        cursor.execute("""
            UPDATE accounts 
            SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (float(amount), account_id))

        # 4. Generate pending payments (installments)
        if installments > 0:
            installment_amount = float(amount) / installments
            tx_date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # First installment is next month
            next_month = tx_date + relativedelta(months=1)
            
            for i in range(installments):
                due_date = next_month + relativedelta(months=i)
                # Adjust to the payment day
                try:
                    final_due_date = due_date.replace(day=payment_day)
                except ValueError:
                    # e.g., if payment day is 31 and month is Feb
                    final_due_date = due_date.replace(day=1) + relativedelta(months=1, days=-1)
                    
                title = f"{description} (Cuota {i+1}/{installments})"
                
                cursor.execute('''
                    INSERT INTO pending_payments (title, type, amount, currency, due_date, account_id, category_id, status)
                    VALUES (?, 'Por Pagar', ?, ?, ?, ?, ?, 'Pendiente')
                ''', (title, installment_amount, currency, final_due_date.strftime('%Y-%m-%d'), account_id, category_id))
            
        conn.commit()
        return True, "Transacción de tarjeta de crédito procesada exitosamente y cuotas generadas."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def register_regular_transaction(date_str, type_str, amount, currency, account_id, destination_account_id, category_id, description, status='Completado', is_recurring=0):
    """
    Standard transaction wrapper moved to service layer for better encapsulation.
    """
    from core.repositories.finance_repo import add_transaction
    return add_transaction(date_str, type_str, amount, currency, account_id, destination_account_id, category_id, description, status, is_recurring)

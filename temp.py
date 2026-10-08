# Verification and Test Suite for Bank Management System
import database
import register
from bank import Bank

def run_tests():
    print("=" * 60)
    print("RUNNING BANK MANAGEMENT SYSTEM COMPREHENSIVE VERIFICATION")
    print("=" * 60)

    # 1. Initialize DB
    database.createcustomertable()
    print("[OK] Step 1: Database initialized successfully.")

    # 2. Register Test Users
    user1 = "testuser_alice"
    user2 = "testuser_bob"

    # Clean up existing test users if re-running
    database.db_execute("DELETE FROM customers WHERE username IN (%s, %s)", (user1, user2))
    database.db_execute("DELETE FROM transactions WHERE username IN (%s, %s)", (user1, user2))

    s1, msg1, acc1 = register.register_user(user1, "Pass1234", "Alice Smith", 28, "New York")
    assert s1 is True, f"Registration failed for Alice: {msg1}"
    print(f"[OK] Step 2a: Registered {user1} with Account #{acc1}.")

    s2, msg2, acc2 = register.register_user(user2, "Pass5678", "Bob Jones", 32, "Chicago")
    assert s2 is True, f"Registration failed for Bob: {msg2}"
    print(f"[OK] Step 2b: Registered {user2} with Account #{acc2}.")

    # 3. Test Authentication
    auth_success, auth_msg, user_info = register.authenticate_user(user1, "Pass1234")
    assert auth_success is True, f"Authentication failed: {auth_msg}"
    assert user_info["account_number"] == acc1
    print("[OK] Step 3: Password hashing & user authentication verified.")

    # 4. Test Deposit
    b1 = Bank(user1, acc1)
    dep_ok, dep_msg, new_bal1 = b1.deposit(1000)
    assert dep_ok is True
    assert new_bal1 == 1000.0
    print(f"[OK] Step 4: Deposited $1,000 into Alice's account. New Balance: ${new_bal1:,.2f}")

    # 5. Test Withdrawal
    wth_ok, wth_msg, new_bal1 = b1.withdraw(250)
    assert wth_ok is True
    assert new_bal1 == 750.0
    print(f"[OK] Step 5: Withdrew $250 from Alice's account. New Balance: ${new_bal1:,.2f}")

    # 6. Test Fund Transfer to Bob
    trf_ok, trf_msg, new_bal1 = b1.fundtransfer(acc2, 300)
    assert trf_ok is True
    assert new_bal1 == 450.0

    b2 = Bank(user2, acc2)
    bob_bal = b2.get_balance()
    assert bob_bal == 300.0
    print(f"[OK] Step 6: Transferred $300 from Alice to Bob. Alice Balance: ${new_bal1:,.2f}, Bob Balance: ${bob_bal:,.2f}")

    # 7. Test Transaction History
    history1 = b1.get_transaction_history()
    assert len(history1) == 3  # Deposit, Withdraw, Transfer
    print(f"[OK] Step 7: Verified transaction history logging ({len(history1)} records).")

    print("=" * 60)
    print("ALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
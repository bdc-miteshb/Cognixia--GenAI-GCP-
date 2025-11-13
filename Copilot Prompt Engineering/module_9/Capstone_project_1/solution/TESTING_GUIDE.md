# Testing Guide - Bug List

## Files with Bugs

1. **database_BUGGY.py** - Backend database operations (5 bugs)
2. **app_BUGGY.py** - Frontend UI (5 bugs)

---

## Database Bugs (database_BUGGY.py)

### BUG 1: Resource Leak in create_user()
- **Location**: Line 62 in `except sqlite3.IntegrityError` block
- **Issue**: Missing `conn.close()` when IntegrityError occurs
- **Impact**: Database connections not closed properly, causing resource leak
- **How to Test**: Try creating duplicate usernames

### BUG 2: SQL Injection Vulnerability in get_user_by_username()
- **Location**: Line 85-86
- **Issue**: Using string formatting instead of parameterized query
- **Impact**: Security vulnerability - SQL injection possible
- **How to Test**: Try entering username like: `admin' OR '1'='1`

### BUG 3: Resource Leak in update_user_email()
- **Location**: Line 149 in `except` block
- **Issue**: Missing `conn.close()` in exception handler
- **Impact**: Database connection not closed on error
- **How to Test**: Force an error while updating email

### BUG 4: Wrong Parameter Order in update_user_password()
- **Location**: Line 170
- **Issue**: Parameters swapped - username and password in wrong order
- **Impact**: Password update will fail or update wrong user
- **How to Test**: Try changing password - it won't work

### BUG 5: Wrong Column Name in get_all_users()
- **Location**: Line 213
- **Issue**: Selecting 'user_name' instead of 'username'
- **Impact**: Query will fail with "no such column" error
- **How to Test**: Call get_all_users() method

---

## Frontend Bugs (app_BUGGY.py)

### BUG 1: No Input Validation in render_login_tab()
- **Location**: Line 52
- **Issue**: Accepts whitespace-only input (no .strip() validation)
- **Impact**: Can login with spaces as username/password
- **How to Test**: Try logging in with "   " (only spaces)

### BUG 2: Syntax Error in render_signup_tab()
- **Location**: Line 83
- **Issue**: Using assignment operator `=` instead of comparison `==`
- **Impact**: App will crash with SyntaxError
- **How to Test**: Try to sign up - page will error

### BUG 3: Wrong Variable Name in render_profile_page()
- **Location**: Line 184
- **Issue**: Using `st.session_state.user_name` instead of `st.session_state.username`
- **Impact**: AttributeError - profile page will crash
- **How to Test**: Navigate to Profile page after login

### BUG 4: Missing st.rerun() in render_settings_page()
- **Location**: Line 253 (after success message)
- **Issue**: No `st.rerun()` after successful password change
- **Impact**: UI doesn't refresh, old password still shown in form
- **How to Test**: Successfully change password, form doesn't clear

### BUG 5: Case Sensitivity Error in render_dashboard()
- **Location**: Line 296
- **Issue**: Checking `page == "home"` instead of `page == "Home"`
- **Impact**: Home page never renders, shows blank dashboard
- **How to Test**: After login, Home page will be blank

---

## Testing Instructions

### Setup
1. Copy `database_BUGGY.py` to `Backend/database.py`
2. Copy `app_BUGGY.py` to `frontend/app.py`
3. Run the application

### Test Scenarios

**Test 1: Create Account**
- Try to create account - should fail with syntax error (Bug 2)

**Test 2: Login**
- After fixing Bug 2, login should work
- Dashboard Home should be blank (Bug 5)

**Test 3: Profile Page**
- Navigate to Profile - should crash (Bug 3)

**Test 4: Change Password**
- Go to Settings, try to change password - won't work (Bug 4 and database Bug 4)

**Test 5: SQL Injection**
- Try logging in with: username = `admin' OR '1'='1` (Bug 2)

**Test 6: Resource Leaks**
- Create multiple duplicate accounts (Bug 1)
- Monitor database connections

**Test 7: Database Query**
- Call get_all_users() function - will fail (Bug 5)

---

## Expected Results After Finding Bugs

All 10 bugs should be identified and documented with:
- Bug location (file and line number)
- Bug type (syntax error, logic error, security vulnerability, etc.)
- Impact on functionality
- Steps to reproduce
- Suggested fix

---

## Bug Severity

**Critical**: Bug 2 (SQL Injection), Bug 4 (Password change doesn't work)
**High**: Bug 3, Bug 5 (App crashes)
**Medium**: Bug 1, Bug 3 (Resource leaks)
**Low**: Bug 1 (Input validation), Bug 4 (UI doesn't refresh)

Happy Testing! 🐛

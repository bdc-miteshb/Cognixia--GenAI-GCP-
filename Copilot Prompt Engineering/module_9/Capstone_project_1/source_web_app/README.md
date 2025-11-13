# Login System - Simple Guide

A login and signup system with a beautiful dashboard. Create accounts, login, and manage your profile!

## 📁 What's Inside

Your project has these folders and files:

```
├── Backend/           (Handles data and authentication)
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   └── database.py
├── frontend/          (The user interface you see)
│   ├── __init__.py
│   └── app.py
├── README.md          (This file)
├── requirements.txt   (List of tools needed)
└── start.sh          (Quick start script)
```

## 🚀 How to Get Started

### Step 1: Install What You Need

Open your terminal or command prompt and type:

```bash
pip install -r requirements.txt
```

This installs Streamlit (the tool that creates the web interface).

### Step 2: Run the Application

From your project folder, type:

```bash
streamlit run frontend/app.py
```

### Step 3: Open in Browser

Your web browser will automatically open to `http://localhost:8501`

If it doesn't open automatically, just copy that link into your browser!

## 🎯 What Can You Do?

### Create an Account
1. Click on the "Sign Up" tab
2. Enter your username, email, and password
3. Confirm your password
4. Click "Sign Up"

### Login
1. Go to the "Login" tab
2. Enter your username and password
3. Click "Login"

### After Logging In

You'll see a dashboard with three pages:

**Home** - View your dashboard with quick stats and recent activity

**Profile** - See your account information and update your email

**Settings** - Change your password and adjust preferences

**Logout** - Click the logout button in the sidebar when you're done

## 📊 Your Data

All your account information is saved in a file called `users.db` that gets created automatically when you first run the app. This file stores:
- Usernames
- Encrypted passwords (for security)
- Email addresses
- When accounts were created

## 🔐 Security

Your passwords are encrypted before being saved, so even if someone looks at the database file, they can't see your actual password!

## ⚙️ Quick Tips

**Change the Port** - If port 8501 is already in use, you can use a different one:
```bash
streamlit run frontend/app.py --server.port 8502
```

**Stop the App** - Press `Ctrl+C` in the terminal to stop the application

**Start Fresh** - Delete the `users.db` file to start over with no accounts

## 🐛 Having Problems?

**"Module not found" error?**
- Make sure you ran `pip install -r requirements.txt`
- Make sure you have the `__init__.py` files in both Backend and frontend folders

**"Port already in use" error?**
- Close any other apps using that port, or use a different port number

**Can't login?**
- Make sure you created an account first using Sign Up
- Check that your username and password are correct (passwords are case-sensitive!)

**Database locked error?**
- Close any other programs that might be using the database
- Restart the application

## 🎨 Want to Customize?

You can easily change things like:
- Minimum password length
- Database file name
- App title and appearance
- Add new pages to the dashboard

Just edit the settings in the Backend/config.py file!

## 📝 Project Structure Explained

**Backend folder** - This is where all the behind-the-scenes work happens:
- Checking if passwords are correct
- Saving and loading user data
- Managing the database

**frontend folder** - This is what you see and interact with:
- The login and signup pages
- The dashboard
- All the buttons and forms

They work together: The frontend shows you things and takes your input, then asks the backend to do the actual work!

## 🎓 Perfect For

- Learning how login systems work
- Building your own projects
- Understanding how frontend and backend connect
- Practicing with databases

## ⚠️ Important Notes

- Your username must be unique
- Passwords must be at least 6 characters long
- Don't forget to logout when you're done!
- The database file is created in your project folder

## 🔄 Updates and Changes

If you want to add new features:
- UI changes go in the frontend folder
- Logic and data changes go in the Backend folder
- Keep them separate for clean code!

## 💡 That's It!

You now have a fully working login system. Enjoy building with it!

Need more help? Check out:
- Streamlit documentation: https://docs.streamlit.io
- Python documentation: https://docs.python.org
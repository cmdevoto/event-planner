# Getting Started With Event Planner App

---

### Step 1: Update .bashrc

Add a little to the path variable: 
`PATH=$PATH:$HOME/.local/bin:$HOME/bin:/home/ec2-user/.linuxbrew/bin`

---

### Step 2: Install Homebrew

When it asks for your password, just ctrl-d. I don't think ramzi ever told us what our password was and I was too lazy to change it.
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

---

### Step 3: Install Python3

This takes a while.
brew install python3

---

### Step 4: Clone the git repository

`git@github.com:cmdevoto/event-planner.git`

---

### Step 5: Create a virtual environment

Do this just inside the event-planner directory, so that if you were to ls you'd also see the eventPlannerApp directory.
`python3 -m venv eventPlannerEnv`

---

### Step 6: Source the Virtual Environment

`source eventPlannerEnv/bin/activate`

---

### Step 7: Install Python Dependencies

`pip3 install -r requirements.txt`

---

### Step 8: Run the app

`python3 app.py`

---

I think that's it?  ¯\_(ツ)_/¯



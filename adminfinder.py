import requests
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import threading

def find_admin_panel(url):
    global stop_search
    global admin_paths
    found_panels = []
    total_paths = len(admin_paths)
    for i, path in enumerate(admin_paths):
        if stop_search:
            break
        full_url = url + path
        progress = (i + 1) / total_paths * 100
        status_var.set(f"Checking: {full_url} ({progress:.2f}%)")
        progress_var.set(progress)
        root.update_idletasks()
        response = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.encoding = 'utf-8'
        if response.status_code == 200:
            found_panels.append(full_url)
    
    if found_panels:
        found_text.delete(1.0, tk.END)
        found_text.insert(tk.END, "\n".join(found_panels))
    else:
        found_text.delete(1.0, tk.END)
        found_text.insert(tk.END, "No admin panels found.")
    status_var.set("Search completed.")
    progress_var.set(0)

def test_xss_vulnerability(url):
    global stop_search
    global xss_payloads
    found_vulnerabilities = []
    total_payloads = len(xss_payloads)
    for i, payload in enumerate(xss_payloads):
        if stop_search:
            break
        full_url = url + payload
        progress = (i + 1) / total_payloads * 100
        status_var.set(f"Testing XSS: {full_url} ({progress:.2f}%)")
        root.update_idletasks()
        response = requests.get(full_url)
        if payload in response.text:
            found_vulnerabilities.append(full_url)
    
    if found_vulnerabilities:
        found_text.delete(1.0, tk.END)
        found_text.insert(tk.END, "XSS Vulnerabilities found:\n" + "\n".join(found_vulnerabilities))
    else:
        found_text.delete(1.0, tk.END)
        found_text.insert(tk.END, "No XSS vulnerabilities found.")
    status_var.set("XSS test completed.")
    progress_var.set(0)

def on_search():
    global stop_search
    stop_search = False
    url = entry.get()
    if url:
        status_var.set("Starting search...")
        root.update_idletasks()
        search_thread = threading.Thread(target=find_admin_panel, args=(url,))
        search_thread.start()
    else:
        messagebox.showwarning("Input Error", "Please enter a website URL.")

def on_xss_test():
    global stop_search
    stop_search = False
    url = entry.get()
    if url:
        status_var.set("Starting XSS test...")
        root.update_idletasks()
        xss_thread = threading.Thread(target=test_xss_vulnerability, args=(url,))
        xss_thread.start()
    else:
        messagebox.showwarning("Input Error", "Please enter a website URL.")

def on_cancel():
    global stop_search
    stop_search = True
    status_var.set("Search canceled.")
    progress_var.set(0)

def load_xss_payloads():
    global xss_payloads
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            xss_payloads = [line.strip() for line in file.readlines()]
        messagebox.showinfo("Success", "XSS payloads loaded successfully.")

def load_admin_paths():
    global admin_paths
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            admin_paths = [line.strip() for line in file.readlines()]
        messagebox.showinfo("Success", "Admin paths loaded successfully.")

# Create the main window
root = tk.Tk()
root.title("Jigen Disuke")

# Apply dark theme
root.configure(bg="#2e2e2e")

# Create and place the widgets
left_frame = tk.Frame(root, bg="#2e2e2e")
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

right_frame = tk.Frame(root, bg="#2e2e2e")
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

label = tk.Label(left_frame, text="Enter the website URL (e.g., http://example.com/):", bg="#2e2e2e", fg="white")
label.pack(pady=10)

entry = tk.Entry(left_frame, width=50, bg="#3e3e3e", fg="white", insertbackground="white")
entry.pack(pady=5)

status_var = tk.StringVar()
status_label = tk.Label(left_frame, textvariable=status_var, bg="#2e2e2e", fg="white")
status_label.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(left_frame, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill=tk.X)

button_frame = tk.Frame(left_frame, bg="#2e2e2e")
button_frame.pack(pady=20)

search_button = tk.Button(button_frame, text="Search", command=on_search, bg="#ffcccc")
search_button.pack(side=tk.LEFT, padx=5)

xss_button = tk.Button(button_frame, text="Test XSS", command=on_xss_test, bg="#ccffcc")
xss_button.pack(side=tk.LEFT, padx=5)

load_xss_button = tk.Button(button_frame, text="Load XSS Payloads", command=load_xss_payloads, bg="#ccccff")
load_xss_button.pack(side=tk.LEFT, padx=5)

load_admin_button = tk.Button(button_frame, text="Load Admin Paths", command=load_admin_paths, bg="#ccccff")
load_admin_button.pack(side=tk.LEFT, padx=5)

cancel_button = tk.Button(button_frame, text="Cancel", command=on_cancel, bg="#fff49b")
cancel_button.pack(side=tk.LEFT, padx=5)

found_text = tk.Text(right_frame, wrap=tk.WORD, height=20, width=50, bg="#3e3e3e", fg="white", insertbackground="white")
found_text.pack(pady=10)

# Initialize stop_search flag and xss_payloads
stop_search = False
admin_paths = [
    'admin/', 'administrator/', 'admin1/', 'admin2/', 'admin3/', 'admin4/', 'admin5/', 'usuarios/', 'usuario/', 
    'administrator/', 'moderator/', 'webadmin/', 'adminarea/', 'bb-admin/', 'adminLogin/', 'admin_area/', 
    'panel-administracion/', 'instadmin/', 'memberadmin/', 'administratorlogin/', 'adm/', 'admin/account.php', 
    'admin/index.php', 'admin/login.php', 'admin/admin.php', 'admin/account/', 'admin_area/admin.php', 
    'admin_area/login.php', 'siteadmin/login.php', 'siteadmin/index.php', 'siteadmin/login.html', 'admin/account.html', 
    'admin/index.html', 'admin/login.html', 'admin/admin.html', 'admin_area/index.php', 'bb-admin/index.php', 
    'bb-admin/login.php', 'bb-admin/admin.php', 'admin/home.php', 'admin_area/login.html', 'admin_area/index.html', 
    'admin/controlpanel.php', 'admin.php', 'admincp/index.asp', 'admincp/login.asp', 'admincp/index.html', 
    'adminpanel.html', 'webadmin.html', 'webadmin/index.html', 'webadmin/admin.html', 'webadmin/login.html', 
    'admin/admin_login.html', 'admin_login.html', 'panel-administracion/login.html', 'admin/cp.php', 'cp.php', 
    'administrator/index.php', 'administrator/login.php', 'nsw/admin/login.php', 'webadmin/login.php', 
    'admin/admin_login.php', 'admin_login.php', 'administrator/account.php', 'administrator.php', 'admin_area/admin.html', 
    'pages/admin/admin-login.php', 'admin/admin-login.php', 'admin-login.php', 'adminpanel.php', 'admincontrol/', 
    'admincontrol/login.php', 'admincontrol/index.php', 'admincontrol/admin.php', 'admincontrol/panel.php', 
    'admincontrol/dashboard.php', 'admincontrol/home.php', 'admincontrol/controlpanel.php', 'admincontrol/admin_login.php', 
    'admincontrol/admin_login.html', 'admincontrol/login.html', 'admincontrol/index.html', 'admincontrol/admin.html', 
    'admincontrol/panel.html', 'admincontrol/dashboard.html', 'admincontrol/home.html', 'admincontrol/controlpanel.html', 'registration/admin.php', 'admin/index.php', 'en/uncat/296-site-admin-login', 'track/admin/index.html', 'admin/index.php', 'admin/home.php', 'nceglibrary/ajax/admin.php?ajax=yes', 'clients/geolocation/admin/index.php' , 'track/admin/index.html'
]
xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>", "<body onload=alert('XSS')>"]

# Run the application
root.mainloop()
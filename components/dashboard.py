from components import dashboard_admin, submit_report

def route_page(choice):
    if choice == "Dashboard Admin":
        dashboard_admin.dashboard_admin()
    elif choice == "Manage Reports":
        dashboard_admin.manage_reports()
    elif choice == "Submit Report":
        submit_report.submit()

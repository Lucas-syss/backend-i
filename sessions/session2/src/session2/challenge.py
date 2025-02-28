def main():
    users = {'jack': 12345, 'sara': 54321}
    
    def register(*args, **kwargs):
        name = kwargs.get('name', input("Input your name: "))
        password = kwargs.get('password', input("Enter a password: "))
        confirm_password = kwargs.get('confirm_password', input("Enter the password again: "))
        
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            return
        
        users[name] = password
        print(f"User {name} successfully registered!")
        print("Updated users:", users)
    print("Current users:", users)
    register()
    #  teste
    #register(name="john", password="password123", confirm_password="password123")
    
    
if __name__ == "__main__":
    main()

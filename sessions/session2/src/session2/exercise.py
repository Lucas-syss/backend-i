def main():
    def countArgs(*args):
        total = sum(args) 
        print(total)
    countArgs(1,2,3,4,5,6,7,8,9,10)
    
    def filterValues(*kwargs):
        values = {x for x in kwargs if x > 5}
        print(values)
    filterValues(2, 6, 10, 1)
    
if __name__ == "__main__":
    main()
    
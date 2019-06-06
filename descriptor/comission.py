class Value:
    def __init__(self):
        self.value = None

    def __get__(self, obj, obj_type):
        print("get")
        return self.value

    def __set__(self, obj, value):
        print("set")
        self.value = value * (1-obj.__dict__['commission'])


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


if __name__ == '__main__':
    new_account = Account(0.23)
    new_account.amount = 1343

    print(new_account.amount)
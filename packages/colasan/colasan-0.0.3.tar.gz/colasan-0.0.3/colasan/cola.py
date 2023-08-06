class Cola:
    def __init__(self):
        self.name = 'Cola'
        self.lastname = 'Variola'
        self.nickname = 'Cola san'

    def whoiam(self):
        print('My name is: {}'.format(self.name))
        print('My lastname is: {}'.format(self.lastname))
        print('My nickname is: {}'.format(self.nickname))

    @property
    def email(self):
        return 'email: {}.{}@gmail.com'.format(self.name.lower(), self.lastname.lower())

    def __str__(self):
        return 'This is a Cola class'

if __name__ == '__main__':
    cola = Cola()
    print(cola)
    # print(cola.name)
    # print(cola.lastname)
    # print(cola.nickname)

    cola.whoiam()
    print(cola.email)

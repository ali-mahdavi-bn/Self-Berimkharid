from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, userName, email, phoneNumber, firstName, lastName, password, isAdmin, type='customer',
                    status='deactivate'):
        if not phoneNumber:
            raise ValueError('user must have a phone number')

        if not email:
            raise ValueError('user must have an email address')

        if not userName:
            raise ValueError('user must have an userName')

        if not firstName:
            raise ValueError('user must have a first name')

        if not lastName:
            raise ValueError('user must have a last name')

        user = self.model(phoneNumber=phoneNumber,
                          userName=userName,
                          email=self.normalize_email(email),
                          firstName=firstName,
                          lastName=lastName,
                          type=type,
                          status=status,
                          isAdmin=isAdmin)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userName, email, firstName, lastName, phoneNumber, password, isAdmin=True, type='superAdmin',
                         status='active'):

        user = self.create_user(phoneNumber=phoneNumber,
                                type=type,
                                status=status,
                                email=email,
                                userName=userName,
                                firstName=firstName,
                                lastName=lastName,
                                password=password,
                                isAdmin=isAdmin)

        user.save(using=self._db)
        return user

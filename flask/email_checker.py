import valid_emails as vm


def perms(word):
    '''All edits that are one edit away from `word`'''
    letters = 'qwertyuiopasdfghjklzxcvbnm'

    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]

    return set(deletes + transposes + replaces + inserts)


class EmailPurifier:
    def __init__(self, emails, valid_emails=[], onlyAdditional=False):
        '''
        Initialises The Instance with emails and empty wrong emails list
        Valid Email domains are stored in valid
        '''
        self.emails = emails
        self.wrong_emails = []
        if onlyAdditional is True:
            self.valid = valid_emails
        else:
            self.valid = vm.valid_emails_list + valid_emails

    def CheckEmails(self, checkTypo=False, fillWrong=True):
        '''Checks Emails in List Wether they are Correct or not'''
        self.wrong_emails = []
        for email in self.emails:
            if self.CheckEmail(email, checkTypo) is False:
                self.wrong_emails.append(email)

    def CheckEmail(self, email, checkTypo=False):
        '''Checks a Single email if it is correct'''
        contents = email.split('@')
        if len(contents) == 2:
            if contents[1] in self.valid:
                return True
        return False

    def CorrectWrongEmails(self, askInput=True):
        '''Corrects Emails in wrong_emails'''
        for email in self.wrong_emails:
            corrected_email = self.CorrectEmail(email)
            self.emails[self.emails.index(email)] = corrected_email

        self.wrong_emails = []


    def SuggestEmails(self):
        self.suggestedmails = []
        for email in self.wrong_emails:
            suggestion = self.SuggestEmail(email)
            self.suggestedmails.append(suggestion)

    def SuggestEmail(self,email):
        contents = email.split('@')
        if len(contents) == 2:
            domain_data = contents[1].split('.')
            for vemail in self.valid:
                alters = perms(vemail.split('.', 1)[0])
                if domain_data[0] in alters:
                        return contents[0] + '@' + vemail

        elif len(contents) == 1:
            for vemail in self.valid:
                if email[len(email) - len(vemail):] == vemail:
                    return email[:len(email) - len(vemail)] + '@' + vemail

            return email+'@gmail.com'

        else:       #more than 1 @, consider first @ and suggest
            email = contents[0]+'@'+contents[1]
            return SuggestEmail(self,email)






    def stats(self):
        print('___STATS___')
        print('Emails = ', self.emails)
        print('Wrong Emails = ', self.wrong_emails)
        print('Valid Domains = ', self.valid)
        print('___END___')

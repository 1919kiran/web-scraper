class Applicant:
    name = "NA"
    profile_link = "NA"
    uni_name = "NA"
    course_name = "NA"
    period = "NA"
    gre = "NA"
    eng_test = "NA"
    eng_test_marks = "NA"
    undergrad_college = "NA"
    undergrad_marks = "NA"
    scoring = "NA"
    experience = "NA"
    status = "NA"

    # ordering the data as string
    def __str__(self):
        # for attr in dir(Applicant):
        #     if not callable(getattr(Applicant, attr)) and not attr.startswith('__') and not None:
        #         applicant += "," + str(self.__dict__.get(attr))
        return self.uni_name + "," + self.course_name + "," + self.period + "," + self.undergrad_marks + "," + \
               self.scoring + "," + self.undergrad_college + "," + self.gre + "," + self.eng_test + "," + \
               self.eng_test_marks + "," + self.experience + "," + self.status + "," + self.name + ","+self.profile_link

    # clean the data and set it to object in case on any exceptions set it to NA
    def __setattr__(self, key, value):
        value = ''.join([i if ord(i) < 128 else '' for i in value])
        try:
            if value:
                self.__dict__[key] = value
        except:
            self.__dict__[key] = "NA"

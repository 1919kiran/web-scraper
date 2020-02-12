class Applicant:
    uni_name = "NA"
    course_name = "NA"
    period = "NA"
    undergrad_college = "NA"
    undergrad_marks = "NA"
    scoring = "NA"
    gre = "NA"
    gre_quant = "NA"
    gre_verbal = "NA"
    eng_test = "NA"
    eng_test_marks = "NA"
    experience = "NA"
    research_level = "NA"
    research_papers = "0"
    status = "NA"
    name = "NA"
    profile_link = "NA"

    # ordering the data as string
    def __str__(self):
        return self.uni_name + "," + self.course_name + "," + self.period + "," + self.undergrad_college \
               + "," + self.undergrad_marks + "," + self.scoring + "," + self.gre + "," + self.gre_quant \
               + "," + self.gre_verbal + "," + self.eng_test + "," + self.eng_test_marks + "," + self.experience \
               + "," + self.research_level + "," + self.research_papers + "," + self.status + "," + self.name \
               + "," + self.profile_link

    # clean the data and set it to object in case on any exceptions set it to NA
    def __setattr__(self, key, value):
        value = ''.join([i if ord(i) < 128 else '' for i in value])
        try:
            if value:
                self.__dict__[key] = value
        except:
            self.__dict__[key] = "NA"

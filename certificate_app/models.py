from django.db import models

from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)

class Training(models.Model):
    course_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)

class Technology(models.Model):
    technology = models.CharField(max_length=100)


class Grade(models.Model):
    name = models.CharField(max_length=10)



class NumberTracker(models.Model):
    last_enroll_no = models.CharField(max_length=100,default='PMS|2025|ST|139|1001') 
    last_verification_no = models.CharField(max_length=100,default='CDPMSINT1001')  

    def __str__(self):
        return f"Enroll: {self.last_enroll_no}, Verif: {self.last_verification_no}"


class Student_data(models.Model):
    name = models.CharField(max_length=100)
    enroll_no = models.CharField(max_length=50, unique=True)
    verification_no = models.CharField(max_length=50, unique=True)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True)
    college = models.CharField(max_length=100)
    training_duration = models.ForeignKey('Training', on_delete=models.SET_NULL, null=True, related_name="+")
    training_course = models.ForeignKey('Training', on_delete=models.SET_NULL, null=True, related_name="+")
    training_technology = models.ForeignKey('Technology', on_delete=models.SET_NULL, null=True, related_name="+")
    start_duration_from = models.DateField()
    end_duration_to = models.DateField()
    grade = models.ForeignKey('Grade', on_delete=models.SET_NULL, null=True)



class Student(models.Model):
    name = models.CharField(max_length=100)
    enroll_no = models.AutoField(primary_key=True)  # Auto-incremented enrollment number
    course = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    duration_from = models.DateField()
    duration_to = models.DateField()
    grade = models.CharField(max_length=10)
    # verification_no = models.AutoField(unique=True)  # Auto-incremented verification number


    def __str__(self):
        return self.name


class Student_award_data(models.Model):
    name = models.CharField(max_length=100)
    sr_no = models.CharField(max_length=50, unique=True)
    award = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    issued_date = models.DateField()
    
    def __str__(self):
        return f"Name: {self.name}, Award: {self.award}"

class NumberTracker_award(models.Model):
    last_sr_no = models.CharField(max_length=100,default='PMS|2025|ST|139|AWD01') 
    
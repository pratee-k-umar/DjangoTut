from django.contrib import admin
from .models import *
from django.db.models import Sum

# Register your models here.

admin.site.register(Recipe)

admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Subject)

class SubjectMarksAdmin(admin.ModelAdmin):
  list_display = ["student", "subject", "marks"]

admin.site.register(StudentSubjectMarks, SubjectMarksAdmin)

class StudentReportCardAdmin(admin.ModelAdmin):
  list_display = ["student", "student_rank", "total_marks", "date_of_reportCard_generation"]
  def total_marks(self, obj):
    student_marks = StudentSubjectMarks.objects.filter(student = obj.student)
    print(student_marks.aggragate(marks = Sum('marks')))
    return 0
admin.site.register(StudentReportCard, StudentReportCardAdmin)
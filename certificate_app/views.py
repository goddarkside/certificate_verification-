from django.shortcuts import render, redirect
from django.conf import settings
from django.http import FileResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont
import os
import io
import uuid

from certificate_app.models import *


def index(request):
    return render(request, "index.html")


# certificate-------------------------------------------------------------------------------

def certificate_form(request):
    courses = Course.objects.all()
    trainings = Training.objects.all()
    grades = Grade.objects.all()
    technology = Technology.objects.all()

    tracker = NumberTracker.objects.first()
    if request.method == "POST":

        name = request.POST.get("name")
        course_id = request.POST.get("course")
        college = request.POST.get("college")
        training_id = request.POST.get("training")
        technology_id = request.POST.get("technology")
        start_duration_from = request.POST.get("duration_from")
        end_duration_to = request.POST.get("duration_to")
        grade_id = request.POST.get("grade")

        course_data = Course.objects.get(id=course_id)
        course=course_data.name
        training_data = Training.objects.get(id=training_id)
        technology_data = Technology.objects.get(id=technology_id)
        training_duration = training_data.duration
        training_course  = training_data.course_name+ " " + technology_data.technology
        grade_data = Grade.objects.get(id=grade_id)
        grade = grade_data.name
        
        
        parts = tracker.last_enroll_no.split('|')
        numeric_part = int(parts[-1])  
        numeric_part += 1 
        parts[-1] = str(numeric_part)  
        enroll_no = '|'.join(parts) 

        
        prefix = ''.join(filter(str.isalpha, tracker.last_verification_no)) 
        num_part = ''.join(filter(str.isdigit, tracker.last_verification_no)) 
        
        num_part = str(int(num_part) + 1)  
        verification_no = prefix + num_part


        request.session['student_data'] = {
            'name': name,
            'course': course_id,
            'college': college,
            'training': training_id,
            'technology': technology_id,
            'start_duration_from': start_duration_from,
            'end_duration_to': end_duration_to,
            'grade': grade_id,
            'enroll_no': enroll_no,
            'verification_no': verification_no
        }
        # Open certificate template
        template_path = os.path.join(settings.BASE_DIR, "certificate_app", "static", "certificate_app", "Official Certificate (1).jpg")
        image = Image.open(template_path)
        draw = ImageDraw.Draw(image)

        # Load a font
        font_path = os.path.join(settings.BASE_DIR, "certificate_app", "static", "certificate_app", "arial.ttf")
        font = ImageFont.truetype(font_path, 30)

        # Write data (you can adjust x,y coordinates)
        draw.text((300, 220), f"{enroll_no}", font=font, fill="black")
        draw.text((1200, 582), f"{name}", font=font, fill="black")
        draw.text((390, 682), f"{course}", font=font, fill="black")
        draw.text((1200, 682), f"{college}", font=font, fill="black")
        draw.text((1000, 790), f"{training_course}", font=font, fill="black")
        draw.text((580, 920), f"{training_duration}", font=font, fill="black")
        draw.text((860, 920), f"{start_duration_from}", font=font, fill="black")
        draw.text((1180, 920), f"{end_duration_to}", font=font, fill="black")
        draw.text((1480, 920), f"{grade}", font=font, fill="black")
        draw.text((1100, 1120), f"{verification_no}", font=font, fill="black")

        # Save certificate
        file_name = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(settings.MEDIA_ROOT, "certificates", file_name)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)

        request.session["certificate_file"] = file_name
        return redirect("certificate_preview")

    context = {
        "courses": courses,
        "trainings": trainings,
        "grades": grades,
        "technologys": technology,
    }
    return render(request, "certificate_app/form.html",context)


def certificate_preview(request):
    file_name = request.session.get("certificate_file")
    cert_url = f"/media/certificates/{file_name}"
    return render(request, "certificate_app/preview.html", {"cert_url": cert_url, "file_name": file_name})


def certificate_download(request, file_name):
    student_data = request.session.get('student_data')

    if student_data:
        name = student_data.get('name')
        college = student_data.get('college')
        course_id = int(student_data.get('course'))
        training_id = int(student_data.get('training'))
        technology_id = int(student_data.get('technology'))
        grade_id = int(student_data.get('grade'))
        enroll_no = student_data.get('enroll_no')
        verification_no = student_data.get('verification_no')

        student = Student_data.objects.create(
                name= name,
                enroll_no= enroll_no,
                verification_no= verification_no,
                course=Course.objects.get(id=course_id),
                college=college,
                training_duration=Training.objects.get(id=training_id),
                training_course=Training.objects.get(id=training_id),
                training_technology=Technology.objects.get(id=technology_id),
                start_duration_from=student_data.get('start_duration_from'),
                end_duration_to= student_data.get('end_duration_to'),
                grade=Grade.objects.get(id=grade_id)
            )
        tracker = NumberTracker.objects.first()
        tracker.last_enroll_no = enroll_no
        tracker.last_verification_no = verification_no
        tracker.save()
    file_path = os.path.join(settings.MEDIA_ROOT, "certificates", file_name)
    return FileResponse(open(file_path, "rb"), as_attachment=True, filename=f"{name}-{college}-{enroll_no}certificate.jpg")





# award -------------------------------------------


def award_form(request):

    tracker = NumberTracker_award.objects.first()

    if request.method == "POST":
        name = request.POST.get("name")
        college = request.POST.get("college")
        date = request.POST.get("date")
        award_name = request.POST.get("award")

        parts = tracker.last_sr_no.split('|')
        last_code = parts[-1]   # "AWD01"
        prefix = ''.join([c for c in last_code if not c.isdigit()])   
        number = ''.join([c for c in last_code if c.isdigit()])       
        numeric_part = int(number) + 1                               
        parts[-1] = f"{prefix}{numeric_part:02d}"                     
        sr_no = '|'.join(parts)

   


        request.session['student_data_award'] = {
            'name': name,
            'college': college,
            'award': award_name,
            'sr_no': sr_no,
            'issued_date': date,
            
        }

         # Open certificate template
        template_path = os.path.join(settings.BASE_DIR, "certificate_app", "static", "award_app", award_name)
        image = Image.open(template_path)
        draw = ImageDraw.Draw(image)

        # Load a font
        font_path = os.path.join(settings.BASE_DIR, "certificate_app", "static", "certificate_app", "arial.ttf")
        font = ImageFont.truetype(font_path, 30)

        # Write data (you can adjust x,y coordinates)
        draw.text((300, 120), f"{sr_no}", font=font, fill="black")
        draw.text((900, 660), f"{name}", font=font, fill="black")
        draw.text((900, 810), f"{college}", font=font, fill="black")
        draw.text((430, 1065), f"{date}", font=font, fill="black")
        
        # Save certificate
        file_name = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(settings.MEDIA_ROOT, "awards", file_name)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)

        request.session["award_file"] = file_name
        return redirect("award_preview")


    return render(request, "award_app/form.html")


def award_preview(request):
    file_name = request.session.get("award_file")
    cert_url = f"/media/awards/{file_name}"
    print(cert_url)
    return render(request, "award_app/preview.html", {"cert_url": cert_url, "file_name": file_name})

def award_download(request, file_name):
    student_data = request.session.get('student_data_award')
    if student_data:
        name = student_data.get('name')
        college = student_data.get('college')
        award = student_data.get('award')
        sr_no = student_data.get('sr_no')
        issued_date = student_data.get('issued_date')
        

        student = Student_award_data.objects.create(
                name= name,
                award= award,
                sr_no=sr_no,
                college=college,
                issued_date=issued_date,
            )
        tracker = NumberTracker_award.objects.first()
        tracker.last_sr_no = sr_no
        tracker.save()
    file_path = os.path.join(settings.MEDIA_ROOT, "awards", file_name)
    return FileResponse(open(file_path, "rb"), as_attachment=True, filename=f"{name}-{award}-{sr_no}-award.jpg")




# verification

def certificate_verification(request):
    if request.method == "POST":
        v_id = request.POST.get("v_id")
        e_id = request.POST.get("e_id")

        if v_id:
            try:
                certificate_data = Student_data.objects.get(verification_no=v_id)
                context = {'certificate_data': certificate_data}
            except Student_data.DoesNotExist:
                context = {'message': 'No certificate found for this verification number.'}
        elif e_id:
            try:
                certificate_data = Student_data.objects.get(enroll_no=e_id)
                context = {'certificate_data':certificate_data,}
            except Student_data.DoesNotExist:
                context = {'message': 'No certificate found for this Enroll number.'}
            
        else:
            context = {'message':"Certificate Not Found.",}

        return render(request, "certificate_verification/certificate_table.html",context)      

    return render(request, "certificate_verification/verification.html")


# def search_certificate(request):
#     query = request.GET.get('query', '')
#     print(query)
    
#     try:
#         student = Student_data.objects.get(verification_no=query)
       
#         data = {
#             "id": student.id,
#             "name": student.name,
#             "verification_no": student.verification_no,
#             # add other fields you want to return
#         }
#         return JsonResponse({"status": "success", "data": data})
    
#     except Student_data.DoesNotExist:
#         return JsonResponse({"status": "error", "message": "Certificate not found"}, status=404)

def  verification_page_open(request):
    return redirect('certificate_verification')


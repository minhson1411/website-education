from django.contrib import messages
from django.shortcuts import redirect, render
from app.models import Categories,Course,Level,Video,UserCourse,Test
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from app.models import Test, Question, UserTestResponse

def BASE(request):
    return render(request,'base.html')

def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    context = {
        'category' :category,
        'course':course,
    }
    return render(request,'Main/home.html',context)

def SINGLE_COURSE(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    context = {
        'category':category,
        'level':level,
        'course':course,
    }
    return render(request,'Main/single_course.html',context)

def filter_data(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')

    if category:
        course = Course.objects.filter(category__id__in = category).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')

    context = {
        'course':course
    }
    t = render_to_string('ajax/course.html',context)
    return JsonResponse({'data':t})

def CONTACT_US(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category':category
    }
    return render(request,'Main/contact_us.html',context)

def ABOUT_US(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category
    }
    return render(request,'Main/about_us.html',context)

def SEARCH_COURSE(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category
    }
    query = request.GET['query']
    course = Course.objects.filter(title__icontains=query)
    context = {
        'course': course,
    }
    return render(request, 'search/search.html', context)

def COURSE_DETAILS(request,slug):
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))

    course_id = Course.objects.get(slug = slug)
    try :
        check = UserCourse.objects.get(user = request.user, course = course_id)
    except UserCourse.DoesNotExist:
        check = None

    course = Course.objects.filter(slug = slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    context = {
        'course':course,
        'category': category,
        'time_duration': time_duration,
        'check' : check,
    }
    return render(request,'course/course_details.html',context)

def TEST(request, slug):
    course_id = Course.objects.get(slug = slug)
    try :
        check = UserCourse.objects.get(user = request.user, course = course_id)
    except UserCourse.DoesNotExist:
        check = None

    course = Course.objects.filter(slug = slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    
    test = Test.objects.filter(course=course).first()

    context= {
        'test': test,
    }
    return render(request,'test/test.html', context)
def SUBMIT_TEST(request, test_id):
    if request.method == 'POST':

        test = Test.objects.get(id=test_id)


        score = 0

        for question in test.question_set.all():
            user_answer = request.POST.get(f'question_{question.id}')
            
            if user_answer:

                
                if user_answer == question.answer:
                    score += 1
                print(f"user_answer: {user_answer}, correct_answer: {question.answer}")

      
                UserTestResponse.objects.create(
                    user=request.user,
                    question=question,
                    user_answer=user_answer
                )
            else:
                pass
        print(f"Final Score: {score}")
        request.session['test_score'] = score


        messages.success(request, f'Your score is {score} out of {test.question_set.count()}')

        return redirect('test_result')

    else:
        return redirect('home')

def test_result(request):

    test_score = request.session.get('test_score', None)


    if test_score is not None:
        context = {
            'test_score': test_score,
        }
        return render(request, 'test/test_result.html', context)
    else:

        return redirect('home')

def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category
    }
    return render(request,'error/404.html',context)

def ADD_COURSE(request,slug):
    course = Course.objects.get(slug = slug)
    i = 1
    if i == 1 :
        course = UserCourse(
            user= request.user,
            course= course,
        )
        course.save()
        messages.success(request,'Tham gia khóa học thành công!')
        return redirect('my_course')
    return render(request,'error/404.html')

def MY_COURSE(request):
    course = UserCourse.objects.filter(user = request.user)

    context = {
        'course':course,
    }
    return render(request,'course/my_course.html',context)

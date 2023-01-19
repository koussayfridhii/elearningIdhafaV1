from django.shortcuts import render,redirect
from Learn.models import Categories,Course,Level,Video,UserCource
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
# Create your views here.


def PAGE_NOT_FOUND(request):

    return render(request,'error/404.html')


def COURSE_DETAILS(request, slug):
    
    
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum = Sum('time_duration'))
    
    course_id = Course.objects.get(slug = slug) 
    try:
        check_enroll = UserCource.objects.get(user = request.user, course =course_id) 
    except UserCource.DoesNotExist:
        check_enroll = None
    

    course = Course.objects.filter(slug = slug)
    if course.exists():
        course = course.first()

    else:
        return redirect('404')

    context = {
        'course': course,
        'category': category,
        'time_duration':time_duration,
        'check_enroll':check_enroll,
    }
    return render(request,'course/course_details.html', context)



def SEARCH_COURSE(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    context = {
        'course':course,
    }
    return render(request,'search/search.html',context)

def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course", kwargs={'slug': self.slug})

def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print(price)


    if price == ['pricefree']:
       course = Course.objects.filter(price=0 )
    elif price == ['pricepaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
       course = Course.objects.all()
    elif categories:
       course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
       course = Course.objects.all().order_by('-id')


    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})




def Base(request):
    return render(request,'base.html')




def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')

    context = {
        'category':category,
        'course':course,
    }
    return render(request,'Main/home.html', context)




def SINGLE_COURSE(request):
    PaidCourse_count = Course.objects.filter(price__gte = 1) .count()
    FreeCourse_count= Course.objects.filter(price = 0).count()
    level = Level.objects.all()
    category = Categories.get_all_category(Categories)
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    context = {
        'category':category,
        'level' :level,
        'course':course,
        'PaidCourse_count':PaidCourse_count,
        'FreeCourse_count':FreeCourse_count,
    }
    return render(request,'Main/single_course.html', context)



def CONTACT_US(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')

    context = {
        'category':category,
        'course':course,
    }
    return render(request,'Main/contact_us.html', context)


def ABOUT_US(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')

    context = {
        'category':category,
        'course':course,
    }
    return render(request,'Main/about_us.html', context)


def CHECKOUT(request, slug):

    course = Course.objects.get(slug = slug)
    
    if course.price == 0:
        course = UserCource(
            user = request.user,
            course = course,
        )
        course.save()
        messages.success(request,'Course are Successfully Enrolled')
        return redirect('mycourse')
    return render(request, 'checkout/checkout.html')


def MYCOURSE(request):

    course = UserCource.objects.filter(user = request.user)

    context ={
        'course': course,
    }
    return render(request, 'course/my_course.html', context)




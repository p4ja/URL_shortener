from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp.models import LongToShort

# Create your views here.
# def index_page(request):
#     context = {
#         "submitted": False  #if value is default false , then if form is submitted, then it will be visible
#     }
#     if request.method=='POST':
#         context["submitted"]=True
#         long_url=request.POST.get('long_url')
#         custom_name=request.POST.get('custom_name')
#
#         context["long_url"]=long_url
#         context["short_url"]=request.build_absolute_uri() + custom_name  #to get short_url+custom_name for eg:https://127.7.7.8000/docs
#         print(long_url)
#         print(custom_name)
#     else:
#         print("user not send anything..")
#
#     return render(request,"index.html",context)
#
# def task_page(request):
#     return render(request,"task.html")


# def index_page(request):
#     context = {
#         "submitted": False,
#         "error":False
#     }
#
#     if request.method == 'POST':
#         long_url = request.POST.get('long_url')  # retrieve long_url from form
#         custom_name = request.POST.get('custom_name')  # retrieve custom_name from form
#
#         try:
#             obj=LongToShort(long_url=long_url,short_url=custom_name)
#             obj.save()
#
#
#         # READ
#             date=obj.date
#             clicks=obj.clicks
#
#             if long_url and custom_name:
#                 context["submitted"] = True
#                 context["long_url"] = long_url
#                 context["short_url"] = request.build_absolute_uri() + custom_name  # create the short URL
#                 context["date"]=date
#                 context["clicks"]=clicks
#                 context["submitted"]=True
#
#             else:
#                 context["error"] = "Both long URL and custom name are required."
#         except:
#             context["error"]=True
#
#
#     return render(request, "index.html", context)


def index_page(request):
    context = {
        "submitted": False,
        "error": False
    }

    if request.method == 'POST':
        long_url = request.POST.get('long_url')
        custom_name = request.POST.get('custom_name')

        if long_url and custom_name:
            # Check if the alias already exists
            if LongToShort.objects.filter(short_url=custom_name).exists():
                context["error"] = True  # Set error if alias is taken
            else:
                try:
                    obj = LongToShort(long_url=long_url, short_url=custom_name)
                    obj.save()

                    # READ
                    date = obj.date
                    clicks = obj.clicks

                    context["submitted"] = True
                    context["long_url"] = long_url
                    context["short_url"] = request.build_absolute_uri() + custom_name
                    context["date"] = date
                    context["clicks"] = clicks
                except Exception as e:
                    print(f"Error saving the object: {e}")
                    context["error"] = True  # Handle any unexpected errors
        else:
            context["error"] = True  # Handle case where long URL or custom name is missing

    return render(request, "index.html", context)


def redirect_url(request,short_url):
    row=LongToShort.objects.filter(short_url=short_url)
    if len(row)==0:
        return HttpResponse("No such url exists..")

    obj=row[0]
    long_url=obj.long_url

    obj.clicks=obj.clicks + 1
    obj.save()
    return redirect(long_url)

def all_analytics(request):
    rows=LongToShort.objects.all()
    return render(request,"all-analytics.html",{'rows':rows})

def display_urls(request):
    rows = LongToShort.objects.all()
    return render(request,"display_urls.html",{'rows':rows})

def delete_urls(request,url_id):
    x=LongToShort.objects.filter(id=url_id)
    x.delete()
    return redirect(display_urls)

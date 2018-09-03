# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View


class OrgListView(View):
    def get(self,request):
        return render(request,'org-list.html',{})

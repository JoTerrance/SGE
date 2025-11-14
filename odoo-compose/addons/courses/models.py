# -*- coding: utf-8 -*-

from odoo import models, fields, api


#create a model called course
class Course(models.Model):
    _name = 'course.course'
    _description = 'Course'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Course Name', required=True)
    description = fields.Text(string='Course Description')
    duration = fields.Integer(string='Duration (hours)')
    course_act = fields.Boolean(string='Active', default=True)
    students = fields.One2many('course.student', 'enrolled_courses', string='Enrolled Students')
    
    

#create a model called student
class Student(models.Model):
    _name = 'course.student'
    _description = 'Student'

    name = fields.Char(string='Student Name', required=True)
    age = fields.Integer(string='Age')
    email = fields.Char(string='Email')
    enrolled_courses = fields.Many2one('course.course', string='Enrolled Course')


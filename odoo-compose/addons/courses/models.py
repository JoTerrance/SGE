# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


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
    dni = fields.Char(string='DNI', required=True)
                       
    age = fields.Integer(string='Age')
    email = fields.Char(string='Email')
    enrolled_courses = fields.Many2one('course.course', string='Enrolled Course')
    sessions = fields.Many2many('course.session', string='Sessions Attended')

    @api.constrains('dni')
    def _check_dni_unique(self):
        for record in self:
            if self.search_count([('dni', '=', record.dni)]) > 1:
                raise  ValidationError("DNI must be unique.")
            


# create a model sessions
class Session(models.Model):
    _name = 'course.session'
    _description = 'Session'

    course_id = fields.Many2one('course.course', string='Course', required=True)
    session_date = fields.Datetime(string='Session Date', required=True)
    duration = fields.Integer(string='Duration (hours)')
    instructor = fields.Char(string='Instructor')
    students = fields.Many2many('course.student', string='Attending Students')


    @api.constrains('session_date')
    def _check_session_date_future(self):
        
        for record in self:
            if record.session_date < datetime.now():
                raise ValidationError("Session date must be in the future.")    


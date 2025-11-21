# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta


#create a model called course
class Course(models.Model):
    _name = 'course.course'
    _description = 'Course'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Course Name', required=True)
    description = fields.Text(string='Course Description', compute='_compute_name')
    duration = fields.Integer(string='Duration (hours)')
    course_act = fields.Boolean(string='Active', default=True)
    students = fields.One2many('course.student', 'enrolled_courses', string='Enrolled Students')
    price = fields.Float(string='Course Price')
    amount_discount = fields.Float(string='Discount Amount')
    total_price = fields.Float(string='Total Price')

    @api.onchange('price', 'amount_discount')
    def _onchange_total_price(self):
        for record in self:
            record.total_price = record.price - record.amount_discount
        #if record.total_price <= record.price:
            # Can optionally return a warning and domains
            return {
                'warning': {
                    'title': "tacaño",
                    'message': "haz un descuento mayor",
                }
            }
        
        


    @api.depends('duration', 'nombre')
    def _compute_name(self):
        for record in self:
            record.description = "Record %s with duration %s" % (record.nombre, record.duration)
    

#create a model called student
class Student(models.Model):
    _name = 'course.student'
    _description = 'Student'

    name = fields.Char(string='Student Name', required=True)
    dni = fields.Char(string='DNI', required=True, compute='_calculate_dni_letter', store=True )

                       
    age = fields.Integer(string='Age')
    email = fields.Char(string='Email', compute='_compute_email ', store=True)
    enrolled_courses = fields.Many2one('course.course', string='Enrolled Course')
    sessions = fields.Many2many('course.session', string='Sessions Attended')

    @api.depends('name', 'age')
    def _compute_email (self):
        for record in self:
            if record.name:
                record.email = record.name.lower().replace(" ", ".")+ str(record.age) + "@example.com"
            else:
                record.email = ""


    @api.depends('dni')
    def _calculate_dni_letter(self):
        letters = "TRWAGMYFPDXBNJZSQVHLCKE"
        for record in self:
            if record.dni and record.dni[:-1].isdigit():
                number = int(record.dni[:-1])
                index = number % 23
                record.dni = record.dni[:-1] + letters[index]
            else:
                record.dni = record.dni

   

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
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', compute='_compute_end_time', store=True)  

    @api.constrains('end_time')
    def _check_end_time_after_start_time(self):
        for record in self:
            if record.end_time and record.start_time and record.end_time <= record.start_time:
                raise ValidationError("End time must be after start time.")
            
    @api.onchange('start_time', 'end_time')
    def _onchange_end_time(self):
        for record in self:
            if record.start_time and record.end_time:
                record.duration = (record.end_time - record.start_time).total_seconds() / 3600
            else:
                record.duration = 0


    @api.depends('start_time', 'duration')
    def _compute_end_time(self):
        for record in self:
            if record.start_time and record.duration:
                record.end_time = record.start_time + timedelta(hours=record.duration)
            else:
                record.end_time = False

    @api.constrains('session_date')
    def _check_session_date_future(self):
        
        for record in self:
            if record.session_date < datetime.now():
                raise ValidationError("Session date must be in the future.")    


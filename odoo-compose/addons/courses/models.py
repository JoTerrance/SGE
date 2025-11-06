# -*- coding: utf-8 -*-

from odoo import models, fields, api


#create a model called course
class Course(models.Model):
    _name = 'course.course'
    _description = 'Course'

    nombre = fields.Char(string='Course Name', required=True)
    description = fields.Text(string='Course Description')
    duration = fields.Integer(string='Duration (hours)')
    active = fields.Boolean(string='Active', default=True)
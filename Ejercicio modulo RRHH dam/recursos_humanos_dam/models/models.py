# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class empleado(models.Model):
    _name = 'recursos_humanos_dam.empleado'
    _description = 'recursos_humanos_dam.empleado'

    nombre = fields.Char(string = "Nombre", required=True)
    apellido1 = fields.Char(string = "1er apellido", required=True)
    apellido2 = fields.Char(string = "2º apellido", required=True)
    nombreCompleto = fields.Char(string = "Nombre completo", compute="getNombre")
    dni = fields.Char(string = "DNI(Sin letra)", required=True)
    fechaNac = fields.Date(string='Fecha de nacimiento', required=True)
    edad = fields.Integer(string="Edad", compute="getEdad")
    sueldoBrutoAnual = fields.Monetary(string = "Sueldo bruto anual", required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)
    fechaInicio = fields.Date(string='Fecha de inicio de contrato', default=fields.Date.today, required=True)
    fechaFin = fields.Date(string='Fecha de fin de contrato')
    estado = fields.Char(string="Estado", compute="getEstado")
    codigoEmpleado = fields.Char(string="Codigo de empleado", compute="getCodigo")
    imagen = fields.Binary(string='Imagen', attachment=True, required=True)
    
    
    @api.depends('nombre','apellido1','apellido2')
    def getNombre(self):
        for emple in self:
            if emple.nombre and emple.apellido1 and emple.apellido2:
                emple.nombreCompleto = f"{emple.nombre} {emple.apellido1} {emple.apellido2}"
            else:
                emple.nombreCompleto = "Sin definir"
            _logger.info(f"Ejecutando método getNombre para el empleado: {emple.id}")

    @api.depends('fechaNac')
    def getEdad(self):
        for emple in self:
            if emple.fechaNac:
                fecha_actual = fields.Date.today()

                # Cálculo de la edad
                emple.edad = fecha_actual.year - emple.fechaNac.year

                # Verifica si el cumpleaños ya pasó este año
                if (fecha_actual.month, fecha_actual.day) < (emple.fechaNac.month, emple.fechaNac.day):
                    emple.edad -= 1
            else:
                emple.edad = 0
            _logger.info(f"Ejecutando método getEdad para el empleado: {emple.id}")

    @api.depends('fechaInicio','fechaFin')
    def getEstado(self):
        for emple in self:
            if emple.fechaInicio:
                if emple.fechaFin:
                    emple.estado = "BAJA"
                else:
                    emple.estado = "ACTIVO"
            else:
                emple.estado = "Sin definir"
            _logger.info(f"Ejecutando método getEstado para el empleado: {emple.id}")

    @api.depends('dni','fechaInicio')
    def getCodigo(self):
        for emple in self:
            if emple.dni and emple.fechaInicio:
                ultimasCincoCifras = emple.dni[-5:]
                fecha = emple.fechaInicio.strftime('%d%m%y')
                emple.codigoEmpleado = f"COD_{ultimasCincoCifras}_{fecha}"
            else:
                emple.codigoEmpleado = "Sin definir"
            _logger.info(f"Ejecutando método getCodigo para el empleado: {emple.id}")




class empresa(models.Model):
    _name = 'recursos_humanos_dam.empresa'
    _description = 'recursos_humanos_dam.empresa'

    cif = fields.Char(string='CIF', required=True)
    nombre = fields.Char(string='Nombre de la Empresa', required=True)
    nombreCompleto = fields.Char(string='Nombre Completo', compute='getNombre', store=True)

    diccionario = {
        'Amazon': 'AMAZON S.A.',
        'Google': 'GOOGLE INC.',
        'Microsoft': 'MICROSOFT CORPORATION',
        'Facebook': 'META PLATFORMS, INC.',
        'Apple': 'APPLE INC.',
        'Tesla': 'TESLA, INC.',
        'Netflix': 'NETFLIX, INC.',
        'IBM': 'INTERNATIONAL BUSINESS MACHINES CORP.',
        'Oracle': 'ORACLE CORPORATION',
        'Intel': 'INTEL CORPORATION',
        'Samsung': 'SAMSUNG ELECTRONICS CO., LTD.',
        'Sony': 'SONY CORPORATION',
        'HP': 'HEWLETT-PACKARD COMPANY',
        'Adobe': 'ADOBE SYSTEMS INCORPORATED',
        'Uber': 'UBER TECHNOLOGIES, INC.'
    }

    @api.depends('nombre')
    def getNombre(self):
        for empre in self:
            if empre.nombre:
                empre.nombreCompleto = empre.diccionario.get(empre.nombre, '')
            else:
                empre.nombreCompleto = "Sin definir"
            _logger.info(f"Ejecutando método getNombre para la empresa: {empre.id}")




class calculadora(models.Model):
    _name = 'recursos_humanos_dam.calculadora'
    _description = 'recursos_humanos_dam.calculadora'

    nombre = fields.Char(string="Tu nombre", required=True)
    sueldoBrutoAnual = fields.Float(string="Sueldo Bruto Anual", required=True)
    numPagas = fields.Selection([
        ('12', '12'),
        ('14', '14'),
    ], string='Nº de Pagas', required=True)
    irpfAnual = fields.Float(string="IRPF Anual", compute='getIrpfAnual')
    irpfMensual = fields.Float(string="IRPF Mensual", compute='getIrpfMensual')
    tasaIrpf = fields.Float(string="Tasa de IRPF(%)", compute='getTasaIrpf')
    mensualidadBruta = fields.Float(string="Mensualidad Bruta", compute='getMensualidadBruta')
    mensualidadNeta = fields.Float(string="Mensualidad Neta", compute='getMensualidadNeta')

    @api.depends('sueldoBrutoAnual')
    def getIrpfAnual(self):
        for calcu in self:
            if calcu.sueldoBrutoAnual:
                tramos_irpf = [
                    (12450, 0.19),  # Primer tramo hasta 12,450 € al 19%
                    (20200, 0.24),  # Segundo tramo hasta 20,200 € al 24%
                    (35200, 0.30),  # Tercer tramo hasta 35,200 € al 30%
                    (60000, 0.37),  # Cuarto tramo hasta 60,000 € al 37%
                    (float('inf'), 0.45)  # Quinto tramo más de 60,000 € al 45%
                ]

                irpfTotal = 0
                baseAnterior = 0

                for limite, porcentaje in tramos_irpf:
                    if calcu.sueldoBrutoAnual > limite:
                        irpfTotal += (limite - baseAnterior) * porcentaje
                        baseAnterior = limite
                    else:
                        irpfTotal += (calcu.sueldoBrutoAnual - baseAnterior) * porcentaje
                        break
                calcu.irpfAnual = irpfTotal
            else:
                calcu.irpfAnual = 0
            _logger.info(f"Ejecutando método getIrpfAnual para el cálculo: {calcu.id}")

        
    @api.depends('irpfAnual','sueldoBrutoAnual')
    def getTasaIrpf(self):
        for calcu in self:
            if calcu.irpfAnual and calcu.sueldoBrutoAnual:
                try:
                    calcu.tasaIrpf = (calcu.irpfAnual/calcu.sueldoBrutoAnual)*100
                except ZeroDivisionError:
                    calcu.tasaIrpf = 0
            else:
                calcu.tasaIrpf = 0
            _logger.info(f"Ejecutando método getTasaIrpf para el cálculo: {calcu.id}")

    @api.depends('irpfAnual','numPagas')
    def getIrpfMensual(self):
        for calcu in self:
            if calcu.irpfAnual and calcu.numPagas:
                try:
                    calcu.irpfMensual = calcu.irpfAnual / float(calcu.numPagas)
                except ZeroDivisionError:
                    calcu.irpfMensual = 0
            else:
                calcu.irpfMensual = 0
            _logger.info(f"Ejecutando método getIrpfMensual para el cálculo: {calcu.id}")

    @api.depends('sueldoBrutoAnual','numPagas')
    def getMensualidadBruta(self):
        for calcu in self:
            if calcu.sueldoBrutoAnual and calcu.numPagas:
                try:
                    calcu.mensualidadBruta = calcu.sueldoBrutoAnual / float(calcu.numPagas)
                except ZeroDivisionError:
                    calcu.mensualidadBruta = 0
            else:
                calcu.mensualidadBruta = 0
            _logger.info(f"Ejecutando método getMensualidadBruta para el cálculo: {calcu.id}")


    @api.depends('sueldoBrutoAnual','irpfAnual','numPagas')
    def getMensualidadNeta(self):
        for calcu in self:
            if calcu.sueldoBrutoAnual and calcu.irpfAnual and calcu.numPagas:
                try:
                    calcu.mensualidadNeta = (calcu.sueldoBrutoAnual - calcu.irpfAnual) / float(calcu.numPagas)
                except ZeroDivisionError:
                    calcu.mensualidadNeta = 0
            else:
                calcu.mensualidadNeta = 0
            _logger.info(f"Ejecutando método getMensualidadNeta para el cálculo: {calcu.id}")
        

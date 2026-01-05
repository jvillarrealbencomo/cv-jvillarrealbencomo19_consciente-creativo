"""
Legacy CV 2019 Routes
Preserves original CV 2019 functionality with all 11 routes
Routes are named to match original Flask function names for compatibility
"""
from flask import Blueprint, render_template

legacy_bp = Blueprint('legacy', __name__, url_prefix='/legacy/cv2019')

# 1. HOME - Introducción
@legacy_bp.route('/', endpoint='fnCargaInicio')
def fnCargaInicio():
    """CV 2019 Home - Introduction and professional summary"""
    return render_template('legacy/inicio2.html')

# 2. EDUCATION - Historia educativa
@legacy_bp.route('/educacion', endpoint='educacion')
def educacion():
    """CV 2019 Education - Degrees and formal education"""
    return render_template('legacy/educacion2.html')

# 3. WORK EXPERIENCE - Experiencia laboral
@legacy_bp.route('/experienciaLaboral', endpoint='experienciaLaboral')
def experienciaLaboral():
    """CV 2019 Work Experience - Job positions and roles"""
    return render_template('legacy/experienciaLaboral.html')

# 4. IT PRODUCTS - Productos informáticos
@legacy_bp.route('/productosInformaticos', endpoint='productosInformaticos')
def productosInformaticos():
    """CV 2019 IT Products - Software and projects created"""
    return render_template('legacy/productosInformaticos.html')

# 5. PERSONAL DATA - Datos personales
@legacy_bp.route('/datosPersonales', endpoint='datosPersonales')
def datosPersonales():
    """CV 2019 Personal Data - Contact information"""
    return render_template('legacy/datosPersonales.html')

# 6. PROGRAMMING SUPPORT - Soporte de programación
@legacy_bp.route('/soporteProgramacion', endpoint='soporteProgramacion')
def soporteProgramacion():
    """CV 2019 Programming Support - Technical skills and tools"""
    return render_template('legacy/soporteProgramacion.html')

# 7. COURSES - Cursos de informática
@legacy_bp.route('/cursosInformatica', endpoint='cursosInformatica')
def cursosInformatica():
    """CV 2019 Courses - Training and professional development"""
    return render_template('legacy/cursosInformaticos.html')

# 8. DOCUMENTS - Main documents page
@legacy_bp.route('/documentos', endpoint='documentos')
def documentos():
    """CV 2019 Documents - Main documents archive page"""
    return render_template('legacy/documentos.html')

# 8a. DOCUMENTS SUBMENU - Titles/Degrees
@legacy_bp.route('/titulos', endpoint='titulos')
def titulos():
    """CV 2019 Titles - Degree certificates and diplomas"""
    return render_template('legacy/titulos.html')

# 8b. DOCUMENTS SUBMENU - Work Certificates
@legacy_bp.route('/constanciasLaborales', endpoint='constanciasLaborales')
def constanciasLaborales():
    """CV 2019 Work Certificates - Employment verification documents"""
    return render_template('legacy/constanciasLaborales.html')

# 8c. DOCUMENTS SUBMENU - Certifications
@legacy_bp.route('/certificaciones', endpoint='certificaciones')
def certificaciones():
    """CV 2019 Certifications - Professional certifications and achievements"""
    return render_template('legacy/certificaciones.html')

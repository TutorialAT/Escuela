from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Text
import os

engine = create_engine('sqlite:///:memory:')
Base = declarative_base()

class Alumno(Base):
    __tablename__ = 'alumno'
    
    id = Column(Integer, Sequence('alumno_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    curso_id = Column(Integer, ForeignKey('curso.id'))
    curso = relationship("Curso",back_populates="alumnos")
    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)

class Curso(Base):
    __tablename__ = 'curso'
    
    id = Column(Integer, Sequence('curso_id_seq'), primary_key=True)
    name = Column(String)

    #relaciones
    alumnos = relationship("Alumno",back_populates="curso")


    horarios = relationship('Horario', back_populates="curso")


    def __repr__(self):
        return "{}".format(self.name)

class Profesor(Base):
    __tablename__ = 'profesor'
    
    id = Column(Integer, Sequence('profesor_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)

    horarios = relationship('Horario',back_populates="profesor")

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)
class Dia(Base):
    __tablename__ = 'dia'
    
    id = Column(Integer, Sequence('dia_id_seq'), primary_key=True)
    day = Column(String)

    horarios = relationship('Horario', back_populates="dia")


    def __repr__(self):
        return "{}".format(self.day)
class Hora(Base):
    __tablename__ = 'hora'
    
    id = Column(Integer, Sequence('hora_id_seq'), primary_key=True)
    rango = Column(String)

    horarios = relationship('Horario',back_populates="hora")
                   
    def __repr__(self):
        return "{}".format(self.rango)

class Horario(Base):
    __tablename__ = 'horario'
    
    id = Column(Integer, Sequence('horario_id_seq'), primary_key=True)
    curso_id = Column(Integer, ForeignKey('curso.id'))
    dia_id = Column(Integer, ForeignKey('dia.id'))
    hora_id = Column(Integer, ForeignKey('hora.id'))
    profesor_id = Column(Integer, ForeignKey('profesor.id'))
    

    curso = relationship('Curso', back_populates="horarios")

    dia = relationship('Dia', back_populates="horarios")

    hora = relationship('Hora',back_populates="horarios")     

    profesor = relationship('Profesor',back_populates="horarios")
                   
    def __repr__(self):
        return "Curso: {}  Dìa: {}  Hora: {}  Profesor: {}".format(self.curso, self.dia,self.hora,self.profesor)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


session.add_all([
    Dia(day='Lunes'),
    Dia(day='Martes'),
    Dia(day='Miércoles'),
    Dia(day='Jueves'),
    Dia(day='Viernes'),
    Dia(day='Sábado'),
    Dia(day='Domingo'),

    Hora(rango='8:00-9:00'),
    Hora(rango='9:00-10:00'),
    Hora(rango='10:00-11:00'),
    Hora(rango='11:00-12:00'),
    Hora(rango='12:00-13:00')
])

text1=("MENÚ PRINCIPAL: \n"+
        "1. Profesor\n"+
        "2. Curso\n"+
        "3. Alumno\n"+
        "0. SALIR\n"+
        "Escriba el número: ")

text2=("ALUMNO: \n"+
        "1. Añadir nuevo \n"+
        "0. MENÚ PRINCIPAL\n"+
        "Escriba el número: ")

text3=("CURSO: \n"+
        "1. Crear \n"+
        "2. Añadir datos de Horario \n"+
        "3. Mostrar ALumnos asociados \n"+
        "4. Mostar Horario de Curso\n"+
        "0. MENÚ PRINCIPAL\n"+
        "Escriba el número: ")

text4=("POFESOR: \n"+
        "1. Añadir nuevo\n"+
        "2. Mostar Horario de profesor\n"+
        "0. MENÚ PRINCIPAL\n"+
        "Escriba el número: ")

def menu():
    global text1
    entrada = input(text1)
    os.system('clear')
    if entrada == '3':
        menu_alumno()
    elif entrada == '2':
        menu_curso()
    elif entrada == '1':
        menu_profesor()
    else:
        print("ESTÀ SALIENDO... GRACIAS Y BUEN DÍA")
        exit()

def menu_alumno():
    global text2,session
    entrada = input(text2)

    def crear():
        os.system('clear')
        print("Seleccione el curso al que pertenecerá:")
        menu_curso(1)
        c_id=input("Escriba el número en la lista: ")
        nombre = input("Ingrese nombre del alumno:")
        apellido = input("Ingrese apellido del alumno:")

        alumnmo_A = Alumno(firstname= nombre, lastname= apellido)
        session.add(alumnmo_A)
        curso_asociado = session.query(Curso)[int(c_id)-1]
        #print(curso_asociado.id, curso_asociado.name)
        alumnmo_A.curso = curso_asociado
        session.commit()
        print('Alumno: ',alumnmo_A)
        print('Curso: ', alumnmo_A.curso)
        input('Presione enter para regresar al menú')
        os.system('clear')
        menu_alumno()
        

    if entrada == '1':
        crear()
    else:
        os.system('clear')
        menu()

def menu_curso(selec=0):
    global text3,session

    def lista_cursos():
        print('Cursos Existentes: ')
        curso_0 = session.query(Curso).order_by(Curso.id)
        if curso_0.count() > 0:
            inde = 0
            for i in curso_0:
                inde += 1
                print ("    "+str(inde)+") " + str(i))
        else:
            os.system('clear')
            print ('    NO existen cursos, primero cree uno\n\n>>Regresando al menú principal\n')
            menu()
    def lista_dias():
        dia_0 = session.query(Dia).order_by(Dia.id)
        inde = 0
        for i in dia_0:
            inde += 1
            print ("    "+str(inde)+") " + str(i))

    def lista_horas():
        hora_0 = session.query(Hora).order_by(Hora.id)
        inde = 0
        for i in hora_0:
            inde += 1
            print ("    "+str(inde)+") " + str(i))

    def crear():
        nombre = input("Ingrese nombre de curso: ")
        curso_0 = Curso(name=nombre)
        session.add(curso_0)
        os.system('clear')
        lista_cursos()
        input('Presione enter para regresar al menú\n')
        os.system('clear')
        menu_curso()

    def edit_horario():
        os.system('clear')
        print("Seleccione un curso de la lista:")
        lista_cursos()
        c_id=input("Escriba el número en la lista: ")
        print("\nSeleccione el dìa:")
        lista_dias()
        d_id=input("Escriba el número en la lista: ")
        print("\nSeleccione la hora:")
        lista_horas()
        h_id=input("Escriba el número en la lista: ")
        print("\nSeleccione un profesor:")
        menu_profesor(1)
        p_id=input("Escriba el número en la lista: ")

        horario_A = Horario()
        curso_A = session.query(Curso).filter_by(id=int(c_id)).first()
        dia_A = session.query(Dia).filter_by(id=int(d_id)).one()
        hora_A = session.query(Hora).filter_by(id=int(h_id)).one()
        profesor_A = session.query(Profesor).filter_by(id=int(p_id)).one()

        horario_A.curso = curso_A
        horario_A.dia = dia_A
        horario_A.hora = hora_A
        horario_A.profesor = profesor_A

        input('Presione enter para regresar al menú')
        os.system('clear')
        menu_curso()

    def list_alum():

        os.system('clear')
        print("Seleccione un curso de la lista:")
        lista_cursos()
        c_id=input("Escriba el número en la lista: ")

        alumno_0 = session.query(Alumno,Curso).order_by(Curso.id)
        if alumno_0.count() > 0:
            for a,b in alumno_0.\
                filter(Alumno.curso_id==Curso.id).\
                filter(Curso.id==int(c_id)).\
                all():
                print (a,' : Curso ',b)
        else:
            os.system('clear')
            print ('    NO hay alumnos asociados\n\n>>Regresando al menú principal\n')
            menu()
        input('Presione enter para regresar al menú')
        os.system('clear')
        menu_curso()

    def list_horario():
        os.system('clear')
        print("Seleccione un curso de la lista:")
        lista_cursos()
        print("    0) TODOS")
        c_id=input("Escriba el número en la lista: ")
        os.system('clear')
        if c_id != '0':
            for a in session.query(Horario).join(Curso).filter(Curso.id == int(c_id)).all():
                print (a)
            if (session.query(Horario).join(Curso).filter(Curso.id == int(c_id)).count() == 0):
                print('No se hallaron datos')
        else:
            for a in session.query(Horario).all():
                print (a)
                
        input('Presione enter para regresar al menú')
        os.system('clear')
        menu_curso()

    if selec == 0:
        
        entrada = input(text3)
        if entrada == '1':
            crear()
        elif entrada == '2':
            edit_horario()
        elif entrada == '3':
            list_alum()
        elif entrada == '4':
            list_horario()
        else:
            os.system('clear')
            menu()

    elif selec == 1:
        lista_cursos()

def menu_profesor(select=0):
    global text4,session

    def lista_profesor():
        print('Profesores Registrados: ')
        profesor_0 = session.query(Profesor).order_by(Profesor.id)
        if profesor_0.count() > 0:
            inde = 0
            for i in profesor_0:
                inde += 1
                print ("    "+str(inde)+") " + str(i))
        else:
            os.system('clear')
            print ('    NO hay profesores registrados, primero añada uno\n\n>>Regresando al menú principal\n')
            menu()
    def crear():
        os.system('clear')
        nombre = input("Ingrese nombre del profesor: ")
        apellido = input("Ingrese apelllido del profesor: ")
        profesor_0 = Profesor(firstname= nombre, lastname= apellido)
        session.add(profesor_0)        
        input('Presione enter para regresar al menú\n')
        os.system('clear')
        menu_profesor()

    def list_horario():

        os.system('clear')
        print("Seleccione un profesor:")
        lista_profesor()
        p_id=input("Escriba el número en la lista: ")
        os.system('clear')
        if p_id != '0':
            for a in session.query(Horario).join(Profesor).filter(Profesor.id == int(p_id)).all():
                print (a)
            if session.query(Horario).join(Profesor).filter(Profesor.id == int(p_id)).count() == 0:
                print('No se hallaron datos')
        else:
            for a in session.query(Horario).all():
                print (a)
                
        input('Presione enter para regresar al menú')
        os.system('clear')
        menu_profesor()       

    if select == 0:
        entrada = input(text4)
        if entrada == '1':
            crear()
        elif entrada == '2':
            list_horario()
        else:
            os.system('clear')
            menu()
    elif select == 1:
        lista_profesor()
menu()

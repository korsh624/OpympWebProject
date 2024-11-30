from db import DatabaseManager


def addAlg(FORM, example, tema):
    base=DatabaseManager('base.db')
    base.create_tables()
    base.query('INSERT INTO alg (FORM, example, tema ) VALUES (?, ?, ?)',(FORM, example, tema))
    
#addAlg('a^2 - b^2 = (a - b)*(a + b)' , "2^2 - 4^2 = (2-4)*(2+4)", "Разность квадратов двух чисел")
# addAlg('(a + b)^2 = a^2 + 2ab + b^2' , "(2+4)^2 = 2^2 + 2*2*4 + 4^2", "Квадрат суммы двух чисел")
# addAlg('D = b^2 - 4ac' , "", "Дискриминант")

def addGeom(FORM, example, tema):
    base=DatabaseManager('base.db')
    base.create_tables()
    base.query('INSERT INTO geom (FORM, example, tema) VALUES (?, ?, ?)',(FORM, example, tema))


#addGeom('S^2 = p(p - a)(p - b)(p - c)' , "S^2 = 11(11-7)(11-5)(11-6)", "теорема Герона")
# addGeom('/' , "/", "/")

def getTable(nameTable):
    base=DatabaseManager('base.db')
    base.create_tables()
    res=base.fetchall(f'SELECT * FROM {nameTable}')
    return res

# print(getTable('geom'))

def addFiz(FORM, example, tema):
    base=DatabaseManager('base.db')
    base.create_tables()
    base.query('INSERT INTO fiz (FORM, example, tema) VALUES (?, ?, ?)',(FORM, example, tema))
    

#addFiz('F = G*m1*m2/r^2' , "F - сила тяготения, G - гравитационная постоянная, равная 6,67*10^-11,  m1 - масса первого тела,  m2 - масса второго тела, r - расстояние между телами",  "закон всемирного тяготения")
# addFiz('F = ma',"a - ускорнение тела, F - равнодействующая сил, m - масса","второй закон Ньютона")
# addFiz('V = V0 + at',"V0 - начальная скорость, a - ускорнение тела,t - время","cкорость при равноускоренном движении")
# addFiz('S = V0t + at^2/2',"V0 - начальная скорость, a - ускорнение тела, t - время", "перемещение при равноускоренном движении")
def addInf(FORM, example, tema):
    base=DatabaseManager('base.db')
    base.create_tables()
    base.query('INSERT INTO inf (FORM, example, tema) VALUES (?, ?, ?)',(FORM, example, tema))
    

#addInf('N = 2^i' , "количество символов в алфавите, которое вычисляется по формуле", 'Мощность алфавита')
# addInf('a^2 - b^2 = (a - b)*(a + b)' , "2^2 - 4^2 = (2-4)*(2+4)", "Разность квадратов двух чисел")
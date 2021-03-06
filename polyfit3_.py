#encoding: utf-8

from scipy.optimize import curve_fit
import numpy as np
import itertools
import matplotlib.pyplot as plt
#from sklearn.metrics import r2_score

def score(y,ya): 
    return np.corrcoef(y,ya)[0, 1]**2
    #return r2_score(y,ya) # або
    #return np.sqrt(np.mean((y-ya)**2))
    #return np.max(np.sqrt((y-ya)**2))
    
def poly(x, A, P):
    """Значення полінома з коефіцієнтами A і степнями P"""
    comp=[a*x**p for a,p in zip(A,P)] # доданки полінома
    return sum(comp) # значення полінома a[0]+a[1]*x+a[2]*x**2

def pfit(x, y, P, Z):
    """Апроксимація поліномом з степенями P з врахуванням вектора занулення Z"""
    def polyz(x, *A): # Поліном з коефіцієнтами A з їх зануленням вектором Z"""
        A=[a*z for a,z in zip(A,Z)] # коефіцієнти полінома з врахуванням занулення
        return poly(x, A, P)
        
    A, cov = curve_fit(polyz, x, y, p0=Z) # апроксимувати нелінійним методом найменших квадратів
    s=score(y,poly(x, A, P)) # внутрішній критерій - наскільки добре p описує точки x,y
    return A, s # коефіцієнти полінома і R**2

def shuffle(x,y): # випадкове перемішування даних
    z=np.array(list(zip(x,y)))
    np.random.shuffle(z)
    return z[:,0], z[:,1]

def crossValidation(x, y, P, Z):
    """Повертає узагальнений критерій"""
    # ділимо дані на групи
    A,s0=pfit(x,y,P,Z) # підгонка усього
    x,y=shuffle(x,y)
    x1,y1=x[0::2],y[0::2] # непарні
    x2,y2=x[1::2],y[1::2] # парні
    A1,s01=pfit(x1,y1,P,Z) # підгонка групи 1
    s1=score(y2, poly(x2,A1,P))
    A2,s02=pfit(x2,y2,P,Z) # підгонка групи 2
    s2=score(y1, poly(x1,A2,P))
    s3=score(poly(x,A1,P), poly(x,A2,P))
    #return np.mean([s0,s1,s2]) # або 
    #return np.mean([s0,s1,s2,s3])
    #return np.mean([s01,s1])
    return s1+s2+s3 #s01+s02+s0+s1+s2+s3

def combi(x,y,Np=4):
    """Комбінаторний алгоритм пошуку моделі
    x,y - координати емпіричних точок
    Np - максимальний степінь полінома"""
    P=range(Np+1) # степені полінома [0,1,2,3,...]
    res=[] # результати
    # усі можливі комбінації
    for Z in itertools.product([0,1],repeat=Np+1):
        #Z - список для занулення коефіцієнтів (1,1,0,...)
        if any(Z[1:]): # окрім поліномів f=0 та f=const
            res.append([Z, crossValidation(x,y,P,Z)]) # узагальнений критерій
    res.sort(key=lambda x: x[1], reverse=True) # сортуємо за спаданням score
    return res # відсортований список Z, score

def plot(x,y,Z,xmin=None,xmax=None):
    """Рисує дані і поліном Z"""
    Np=len(Z)-1
    P=range(Np+1)
    A,s=pfit(x, y, P, Z)
    print "A, R**2 = ", A,s
    plt.plot(x,y,'ro')
    if xmin==None: xmin=x.min()
    if xmax==None: xmax=x.max()
    x_=np.linspace(xmin,xmax,500)
    y_=poly(x_,A,P)
    plt.plot(x_,y_,'k-',linewidth=2)    
    plt.show()

##
if __name__=='__main__': # приклад використання
    # координати емпіричних точок
    #x = np.arange(0,12)
    #y = np.array([-3,-2,2,8,13,16,17,17,13,8,2,-1])
    x = np.arange(0,365)
    y = np.array([4.6, 3.9, 3.4, 1.7, -1.1, 4, 6.5, 3, -0.8, -0.9, 1.3, -0.4, -2.3, -5.9, -9.2, -10.6, -4.2, -0.6, 3.2, -0.5, -1.3, -3.4, -5.1, -7.6, -4.9, -7.1, -5.4, 0, 6.9, 5, 3.8, 3.8, 7.1, 0.6, -0.4, -2.6, -7.3, -2.5, 0.4, -0.8, -1.9, -2.6, -2.3, -0.9, -1.6, -2.3, 0.2, -0.3, -0.9, -2.5, -6.5, -1.2, -2, -3.7, -7.2, -10.7, -12.3, -12.3, -12.2, -14.2, -14.1, -9.4, -7, -7.9, -1.1, 2.6, 5.3, 4.8, 4.5, 6.7, 7.6, 7.9, 9.5, 6.1, 5.7, -2.2, -8.3, -6.7, -4.8, -2.2, -2, -5.1, -1.8, 0.9, 0.1, 5.1, 3.2, 2.3, 7, 9.4, 7.4, 3.9, 8.9, 13.8, 15.8, 10.4, 11.1, 11, 14.1, 16.9, 16.5, 15.4, 17.1, 18.6, 16.4, 15.4, 17.2, 15.2, 16, 12.5, 19, 17, 13.8, 16.9, 18.9, 15.1, 12.7, 15.9, 17.9, 17.6, 21, 20.7, 16.3, 19.8, 19.1, 16.4, 15.5, 16.2, 18.1, 17.6, 15.1, 15.7, 12.7, 12, 12.3, 15.4, 15, 14.4, 14.8, 15.1, 15.2, 18.2, 20.6, 18.9, 17.1, 21, 18.2, 17.8, 20.2, 20.9, 20, 20.9, 19.3, 19.6, 21.3, 22.9, 18.1, 17.1, 19.6, 20.4, 21.3, 20.9, 22.9, 21.6, 17.7, 16.5, 18.6, 16.3, 18.6, 21.8, 22.9, 22.6, 14.6, 10.8, 12.9, 13.7, 15.4, 17.4, 18.7, 18.8, 15.1, 13.4, 14.3, 16.6, 18.9, 20.7, 20.6, 19.8, 19.5, 20.1, 20, 20.9, 21.1, 18.6, 18, 17.8, 17.6, 18.8, 19.8, 20.9, 21.9, 21.9, 21.1, 19.9, 21, 20.4, 20.4, 20.9, 22.1, 21.9, 21.8, 21.8, 23.2, 22.4, 20.1, 21.9, 21.8, 21.6, 20.9, 18.7, 21.3, 21.3, 20.2, 19.5, 21.7, 21.1, 20.6, 18.3, 19.8, 19.4, 21.1, 19.3, 20, 20.2, 21.6, 18.8, 19.8, 18.4, 13.8, 15.4, 15.5, 17, 17.6, 18.4, 18.4, 17.4, 19.7, 18.8, 16.7, 16, 15, 14.1, 18, 17.2, 16.3, 16, 17.1, 16.8, 16, 12.8, 13.3, 16, 15.4, 16, 12.2, 12.2, 11.4, 8.1, 8.4, 11.5, 15.7, 10.1, 7, 6.2, 10.8, 8.9, 9.1, 8.5, 7.9, 12.1, 10.8, 12.4, 10, 8.7, 10.2, 10.9, 9.6, 7.9, 9, 10.5, 8.5, 12.7, 11, 10.5, 7.5, 6.9, 6.3, 6.3, 9.5, 11.1, 11.4, 13.8, 12.1, 15.6, 14.4, 12.3, 11.7, 11.6, 10.1, 9.6, 6.8, 3.9, 4.6, 2.5, 1.7, 5.5, 4.4, 7.5, 6.2, 3, -0.4, 0, -0.1, -1.3, -0.7, -2.3, -3.2, -3.9, 0, 0.2, -2.4, -4.5, -7.5, -12.5, -12.9, -7.6, -2.2, 1.3, 1.8, -1.7, -1.1, 1.8, 1.8, 2.6, 0.7, -0.8, -0.3, -1.1, -2.3, -2.1, -2.3, -2.6, -4.2, -7.2, -6.2, 4.6, 2.4, 0, -1.4, 2.8, 3, 4.9, 2.7, 1.8, 1.3])
    x,y=shuffle(x,y)
    """
    z = np.polyfit(x[::2], y[::2], 50)
    p = np.poly1d(z)
    xp = np.linspace(0, 365, 20000)
    plt.plot(x,y,'ro')
    plt.plot(xp,p(xp),'k')
    plt.show()
    """
    Np=3 # степінь полінома
    res=combi(x,y,Np) # список моделей
    for i in res[:5]:
        print i
    plot(x,y,Z=res[0][0]) # рисуємо найкращий поліном
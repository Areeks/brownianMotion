import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

path = os.getcwd()+'/result/'
isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)


# procedura łączy określenie położeń cząstki podczas błądzenia 
# z procedurą utworzenia wykresu dla tego błądzenia
def main1(iloscKrokow = 1000):
    d = polozenie(iloscKrokow = iloscKrokow)
    wykresBladzenia(d['x'], d['y'], iloscKrokow)
    
    return 


# procedura łączy pozyskanie współrzędnych położenia cząstki w błądzeniu w pewnej ilości symulacji
# ze stworzeniem wykresu położeń końcowych położeń ze wszystkich symulacji
def main2(iloscSymulacji =  1000, iloscKrokow = 1000):
    d = xy_N(iloscSymulacji=iloscSymulacji, iloscKrokow=iloscKrokow)
    wykresPolozenKoncowych(d['x'], d['y'],iloscSymulacji=iloscSymulacji, iloscKrokow=iloscKrokow)
    wykresPolozenKoncowych2(d['x'], d['y'],iloscSymulacji=iloscSymulacji, iloscKrokow=iloscKrokow)

    histogram(d['x'],50, 'x')
    histogram(d['y'],50, 'y')    
        
    return


#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------


def polozenie(dlugoscKroku = 1., iloscKrokow = 10000):
   
    r = dlugoscKroku
    N = iloscKrokow

    # deklarujemy listy współrzędnych cząstki w N krokach:    
    x=[]
    y=[]

    # ustalamy położenie początkowe na punkt (0,0)    
    x.append(0.)
    y.append(0.)
    
    for i in range(iloscKrokow):
        # losujemy kąt z zakresu [0; 2pi), w którym cząstka ma się przemieścić
        kat = 2*np.pi*np.random.rand()
        
        # ustalamy współrzędne położenia w kolejnym kroku:
        x.append(x[-1] + r*np.cos(kat))
        y.append(y[-1] + r*np.sin(kat))
        
    # obliczamy odległoć o jaką się przemieściło ciało (z twierdzenia Pitagorasa):
    d = np.sqrt(x[-1]**2 + y[-1]**2)    
    
        
    
    return {'x': x,'y' : y, 'd': d}


def wykresBladzenia(x, y, iloscKrokow):
    
   color = 'k'
   tytul = 'błądzenie przypadkowe w {} krokach '.format(iloscKrokow)
   
   #x_text = 10
   #y_text = 10
   
   fig, ax = plt.subplots()
   
   ax.plot(x, y, color = color, lw = '0.4')
   
   #ax.plot(x, y, color = color, linewidth = 0, marker = 's', markersize = 3.5, markerfacecolor = markerfacecolor, markeredgewidth = markeredgewidth)
   ax.set_title(label = tytul)
   #ax.text(x_text, y_text, 'N = {}'.format(iloscKrokow))
   
   ax.set_xlabel('x')
   ax.set_ylabel('y')
   fig.savefig(path + "Błądzenie.jpg", dpi = 300)
   
 
      
   return


#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------

# funkcja zwraca połżenia końcowe cząstki błądzącej wszystkich symulacji
# każde błądzenie ma iloscKrokow krokow
def xy_N(iloscSymulacji = 100, iloscKrokow = 1000):
    # każda symulacja ma iloscKrokow w błądzeniu cząstki
    
    x=[]
    y=[]
    d2 = []
    
    for i in range(iloscSymulacji):
        p = polozenie(iloscKrokow = iloscKrokow)
        x.append(p['x'][-1])    # pobieramy współrzędne końcowe położenia cząstki z ostatniej symulacji
        y.append(p['y'][-1])
        
        d = np.sqrt(x[-1]**2 + x[-1]**2)    # całkowite przemieszczenie się cząstki (z tw. Pitagorasa)
        
    
    return {'x': x,'y' : y, 'd': d}


    
def wykresPolozenKoncowych(x,y, iloscSymulacji = 100, iloscKrokow = 1000):
   markersize = 1 
   color = 'k'
   tytul = 'Współrzędne położenia końcowego w {} symulacjach\n ilość kroków {} '.format(iloscSymulacji, iloscKrokow)
   
   fig, ax = plt.subplots()
   
   ax.scatter(x, y, s = markersize, color = color, marker = '.')
   
   ax.set_title(label = tytul)
   
   ax.set_xlabel('x')
   ax.set_ylabel('y')
   fig.savefig(path + 'Polożenie końcowe cząstek.jpg', dpi = 300)


def wykresPolozenKoncowych2(x,y, iloscSymulacji = 100, iloscKrokow = 1000):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    plt.rcParams.update({'font.size': 9, 'font.family': 'serif'})

    hist, xedges, yedges = np.histogram2d(x, y, bins=25, range=[[np.min(x), np.max(x)], [np.min(y), np.max(y)]], density = True)
    
    xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0
    
    dx = dy = 0.5 * np.ones_like(zpos)
    dz = hist.ravel()
    
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz)

    fig.savefig(path + 'Polożenie końcowe cząstek 2.jpg', dpi = 300)



#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------

def d2N(iloscPunktow = 10, iloscSymulacji = 100, poczatkowaIloscKrokow = 1000, symbolZmiennej = 'x'):
    
    import scipy as s
    import scipy.stats as ss    
    
    p = .975    # poziom ufności
    
    d2 = [] # to już będzie wartości średniej
    ud2 = []    # niepewność wyznaczenia wartości d2
    N = []
    
        
    for i in range(iloscPunktow):   # ilość punktów dla wykresu d2 od N
            #ilośc kroków w symulacji jest wielokrotnością początkowej ilości kroków
            #(maksymalna ilość kroków = (ilość punktów - 1)*(początkowa ilość kroków))
        d = []
        N.append(poczatkowaIloscKrokow*(i+1))
        
        
        for j in range(iloscSymulacji):
            d.append(polozenie(iloscKrokow=N[-1])['d'])
            
        dsr = np.mean(d)
        ud = np.array(d).std(ddof = 1)*ss.t.ppf(p, iloscSymulacji - 1)  
    
        d2.append(dsr**2)
        ud2.append(2*dsr*ud)
    
    return {'d2': d2, 'ud2': ud2, 'N': N}


def histogram(x, bins = 50, symbolZmiennej = 'x'):
    fig, ax = plt.subplots()
    ax.hist(x = x, bins = bins)
    ax.set_title(label = 'rozkład zmiennej końcowej {}'.format(symbolZmiennej))
   
    ax.set_xlabel(symbolZmiennej)
    ax.set_ylabel('liczność występowania')
    
    fig.savefig(path + 'histogram położenia {}.jpg'.format(symbolZmiennej), dpi = 300)
    
    return

    
    
    

main1()
main2()
import meanshift as mm
import numpy as np
import cv2
######################################################
def CalculateHist(img,Xpos,Ypos):
#Xposition,Yposition = 200,200
    param = 5
    ListOfHist = []    
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[Xpos-param:Xpos+param, Ypos-param:Ypos+param] = 1

    color = ('b','g','r')
    for i,col in enumerate(color):
        ListOfHist.append(cv2.calcHist([img],[i],mask,[256],[0,256]))
#   histr = cv2.calcHist([img],[i],mask,[256],[0,256])
#   ListOfHist.append(cv2.calcHist([img],[i],mask,[256],[0,256]))
#   plt.plot(histr,color = col)
#   plt.xlim([0,256])
#plt.show()
    return ListOfHist

def DistOfHist(ListOfHist1,ListOfHist2):
    out = 0
    for i in range(3):
        var = cv2.compareHist(ListOfHist1[i],ListOfHist2[i],2)
        out +=var
#        if out <= var:
#           out = var
            
    return out

######################################################

class Particle:          
      def __init__(self, Xcoord , Ycoord  ):
          self.x = Xcoord
          self.y = Ycoord
          self.w = 0
          self.c = 0
            
      def weight(self,img,EtalonHist):
          self.w = DistOfHist(EtalonHist,CalculateHist(img,self.y,self.x))
            
      
#      def NormaliseWeight(self,mass):
#          self.w = self.w/mass
#          #self.w =1-self.w
      
      def __del__(self):
          pass
          #print("удалился")


############################################################


class Particles:
      def __init__(self):
          self.list = []
          self.num_particles = 0
                
      
      def add(self,A):
          self.list.append(A)
          self.num_particles +=1 
          
      
      
      def normalise(self,img,EtalonHist):
          mass = 0
          for i in self:
              i.weight(img,EtalonHist)
              mass += i.w
          self.quantil = mass/self.num_particles
      
      
      
      def __iter__(self):
          self.count = 0
          return self

      def __next__(self):
          if self.count == self.num_particles:
                  raise StopIteration
          self.count += 1
          return self.list[self.count - 1]
          
      def __del__(self):
          pass
          #print("удалил")   
          
      def FindParticle(self):          
          tixe = 0
          while tixe == 0:
                quant = 5*self.quantil*np.random.random_sample()+self.quantil
                for i in self:
                    if i.w >= quant:
                       tixe = 1
                       break 
          return i

      def meanshift(self,oldimg,newimg):
          for i in self:
              xx,yy,w,h = mm.meanshift(i,oldimg,newimg)
              i.x = xx+5
              i.y = yy+5
             





def CreateParticles(x,y):
    num_particles = 33
    Cloud = Particles()
    for i in range(num_particles):
        Xpos = np.random.random_integers(-2,2)+x
        Ypos = np.random.random_integers(-2,2)+y                        
        particle = Particle(Xpos,Ypos)
        Cloud.add(particle)
    return Cloud


def drift(OldCloud):
    NewCloud = Particles()
    for i in range(OldCloud.num_particles):
        oldparticle = OldCloud.FindParticle()
        newparticle = Particle(oldparticle.x+int(11 * np.random.randn() + 0),oldparticle.y+int(11 * np.random.randn() + 0))
        NewCloud.add(newparticle)
    return NewCloud

def resample(OldCloud):
    NewCloud = Particles()
    for i in range(OldCloud.num_particles):
        oldparticle = OldCloud.FindParticle()
        newparticle = Particle(oldparticle.x+int(3 * np.random.randn() + 0),oldparticle.y+int(3 * np.random.randn() + 0))
        NewCloud.add(newparticle)
    return NewCloud


#############################################################

    

    
          
       
              








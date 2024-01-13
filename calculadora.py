# Novo Código
'''
Funcionalidades
1 - > Potênciação
2 - > Porcentagem
3 - > Entry / Digitação por teclado
4 - > Resolver expressão com enter do teclado
5 - > Apagar ultimo elemento da expressão

Configurações
1 - > Estilização
2 - > Concerto de alguns bugs, como não considerar números com ponto flutuante
3 - > Agora a Calculadora funciona tanto para ints como para floats
4 - > Troca de botões
5 - > Congfiruação mais intuitiva, como a estilização de botões e cores na interface gráficas
'''

from tkinter import * # importa toda biblioteca do tkinter
from tkinter import ttk
from ttkthemes import ThemedStyle

class Node: # Representação do nó para abordar a informação
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
    #END def __init__
# END class Node

class ExpressionTree: # Árvore - O cerebro como chegar no primeiro elemento, Raiz da árvore

    def __init__(self, levels):
        self.root = None
        self.levels = levels
    #END def __init__

    # Adiciona um nodo na árvore, respeitando a expressão e a precedência de operadores
    def add(self, value): 
        if self.root is None:
            self.root = Node(value)
        else:
            self._add(self.root, value)

    # Método auxiliar do add para que se possa usar a recursão com o nodo raiz
    def _add(self, node, value):
        if self.levels.get(value, 0) >= self.levels.get(node.value, 0):
            new_node = Node(value)
            new_node.left = node
            self.root = new_node
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._add(node.right, value)

    def calc(self): # Calcula a expressão baseada ná árvore construida, organizando as precedências aritméticas
        return self._calc(self.root)
    # END def calc

    # Método auxiliar do calc, novamente para utilizar a recursão com o nodo raiz
    def _calc(self, node):

        if node.left is None and node.right is None:
            return float(node.value)
        else:
            result = 0.0

            if node.value == '^':
                result = self._calc(node.left) ** self._calc(node.right)
            elif node.value == '/':
                result = self._calc(node.left) / self._calc(node.right)
            elif node.value == 'x':
                result = self._calc(node.left) * self._calc(node.right)
            elif node.value == '+':
                result = self._calc(node.left) + self._calc(node.right)
            elif node.value == '-':
                result = self._calc(node.left) - self._calc(node.right)
            elif node.value == '%':
                result = self._calc(node.left) * (self._calc(node.right) / 100)
            
            return result
    # END def _calc
# END class ExpressionTree

class Calculadora: # definindo uma classe Claculadora
  def __init__(self): # definindo um inicializador
    # CONFIGURAÇÕES
    MIN_WIDTH = 300
    MIN_HEIGHT = 400

    MAX_WIDTH = int(MIN_WIDTH*1.3) # MIN_WIDTH + 30%
    MAX_HEIGHT = int(MIN_HEIGHT * 1.3)  # MAX_HEIGHT + 30%

    TOP_RATIO = 1
    MIDDLE_RATION = 7
    BOTTON_RATION = 2

    TOP_HEIGHT = int(MIN_HEIGHT * TOP_RATIO/10) # 10% of MIN_HEIGHT
    MIDDLE_HEIGHT = int(MIN_HEIGHT * MIDDLE_RATION/10) # 70% of MIN_HEIGHT
    BOTTON_HEIGHT = int(MIN_HEIGHT * BOTTON_RATION/10) # 20% of MIN_HEIGHT

    TOP_FRAME_FONT = 'Courier 22 bold'
    MIDDLE_FRAME_FONT = 'Courier 20 bold'
    BOTTOM_FRAME_FONT = 'Courier 22 bold'

    self.currentNumber = '0'
    self.OPERATORS_LEVEL = {
        '^':1,
        'x':1,
        '/':1,
        '+':2,
        '-':2,
        '%':3
    }

    # CODIGO DA JANELA
    self.window = Tk() # método do objeto Tk
    root = self.window # para abreviar a chamada
    root.title('Minha primeira calculadora - UFOB')
    root.minsize(width=MIN_WIDTH, height=MIN_HEIGHT)
    root.maxsize(width=MAX_WIDTH, height=MAX_HEIGHT)
    
    #Estilização - Configuração Nova - Deixando a interface mais moderna e customizavel
    self.style = ThemedStyle(self.window)
    self.style.set_theme('breeze') # Pode-se escolher diversos temas
    

    # FRAME - TOP, MIDDLE e BOTTOM
    topFrame = Frame(  # Definindo o objeto Frames que vem do Tk
      root,
      width = MIN_WIDTH,
      height = TOP_HEIGHT,
      bg='black',
      border=1,
    ) # Este Frame posteriormente será aplicado no topo da Interface

    middleFrame = Frame(  # Definindo o objeto Frames que vem do Tk
      root,
      width=MIN_WIDTH,
      height=MIDDLE_HEIGHT,
      pady=1
      #bg='green'
    )  # Frame onde os botões númericos e operadores se encontraram

    bottomFrame = Frame(  # Definindo o objeto Frames que vem do Tk
      root,
      width=MIN_WIDTH,
      height=BOTTON_HEIGHT,
      bg='blue'
    )  # Frame onde ficará os botões principais como limpar e "="

    # n - Nort => topo
    # e - East => direita
    # w - West => esquerda
    # s - South => baixo
    topFrame.grid(row=0, column=0, stick = 'news')  # Esta frame esta onde? linha 0 e coluna 0
    middleFrame.grid(row=1, column=0, stick = 'news')  # Esta frame esta onde? linha 0 e coluna 0
    bottomFrame.grid(row=2, column=0, stick = 'news')  # Esta frame esta onde? linha 0 e coluna 0

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=TOP_RATIO)
    root.rowconfigure(1, weight=MIDDLE_RATION)
    root.rowconfigure(2, weight=BOTTON_RATION)

   #- PARTE 02
   # BUILD CONSTRUIR OS FRAMES DA CALCULADORA
    self._BuildTopFrameContent(topFrame, TOP_FRAME_FONT) # É um Método Para construir o conteudo do topo
    self._BuildMiddleFrameContent(middleFrame, MIDDLE_FRAME_FONT)  # É um Método Para construir o conteudo do topo
    self._BuildBottomFrameContent(bottomFrame, BOTTOM_FRAME_FONT)  # É um Método Para construir o conteudo do topo

    # INICIA CALCULADORA
    self.window.mainloop() # inicia a calculadora
  #END def __init__

  def _BuildTopFrameContent(self, frame: Frame, fontConfig): # criando o método
                                 #frame: Frame é um objeto da classe frame
                                 
      # Nova configuração, ao invés de utilizar uma label, a adoção de uma entry se torna mais vantajosa e eficiênte
      # Imagine que você queira resolver cálculos de forma rápida, não resolvemos as contas apertando os botões para
      # A digitação e sim teclamos a expressão, e para isso, a entry se faz muito útil                           
      self.entry_display = Entry( # self para poder acessar de fora, onde tiver acesso ao self.
          frame,
          justify='right',
          font=fontConfig # configuração da fonte, está nas configurações variáreis
      ) # entry display, =  Objeto Entry, filha de top frame

      # Configurando um bind para acelerar o processo de resolução
      self.entry_display.bind('<Return>', self._btn_eq_action)
      self.entry_display.bind('<BackSpace>', self._btn_clr_last_action)

      self.entry_display.grid(row=0, column=0, sticky='news') # posicionar e mostrar na tela  # sticky='news' estica e ajusta a tela.
      frame.columnconfigure(0, weight=1)# ajustar no local toda janela (depois do ponto mostra os métodos que este objeto tem )
      frame.rowconfigure(0, weight=1)
  # END def _BuildTopFrameContent

  # Cria o método onde é construido os botões do Middle Frame, que será os botões numéricos e operadores
  # e configurando o layout de cada botão, no caso o grid, configurando linha e coluna.
  def _BuildMiddleFrameContent(self, frame: Frame, fontConfig):

     buttons = [
         ['7', '8', '9', '/'],
         ['4', '5', '6', 'x'],
         ['1', '2', '3', '-'],
         ['0', '^', '%', '+'],
     ]

     for ridx, row in enumerate(buttons):
         frame.rowconfigure(ridx, weight=1)

         for cidx, col in enumerate(row):
             frame.columnconfigure(cidx, weight=1)

             if col !=' ':
                 # Utilização do ttk button, pelo o simples motivo que o tema só se aplica nos widgets do ttk
                 btn = ttk.Button(
                     frame,
                     text = col,
                     command= lambda x = col: self._btn_NoOp_action(x)# um unico metodo para tratar cada botão
                 )
                 btn.grid(row=ridx, column=cidx, sticky='news')
                 
     self.style.configure('TButton', font=fontConfig)
         # END for cidx
     #END for ridx
  # END def _BuildMiddleFrameContent
  
  # Método que insere os valores dos botões e faz o tratamento das expressões evitando divisões por zero ou
  # outros problemas
  def _btn_NoOp_action(self, value): 
        
      currentValues = self.entry_display.get()  
        
      if currentValues=='Division Error':
          self.entry_display.delete(0,'end')
          self.entry_display.insert(END, '0')

      if value.isdigit(): # número

         if self.currentNumber.startswith('0'):
             self.currentNumber = value
             self.entry_display.delete(0,'end')
             self.entry_display.insert(END, currentValues[:-1])
         else:
             self.currentNumber += value

      else: # Operador
          
          if not currentValues[-1].isdigit(): # se não for um digito
              self.entry_display.delete(0, 'end')
              self.entry_display.insert(END, currentValues[:-1])

          self.currentNumber = ''
      
      self.entry_display.delete(0,'end')
      self.entry_display.insert(END, currentValues + value)
  #END def _btn_NoOp_action
  
  # Método que constrói os botões principais na parte debaixo da interface, e configurando seus layouts
  # no caso o grid
  def _BuildBottomFrameContent(self, frame: Frame, fontConfig):  # criando o método
      btn_clr = ttk.Button( # Bottom é filho da frame
        frame,
        text='Limpar', # Texto que queremos mostrar,
        style='Limpar.TButton',
        command=self._btn_clr_action # cada vez que clicamos no botão ele tem uma ação é um método
      )
      
      self.style.configure('Limpar.TButton', font=fontConfig, foreground='red')
      
      btn_eq = ttk.Button(
        frame,
        text='=',
        style='Result.TButton',
        command=self._btn_eq_action
      )
      btn_clr.grid(row=0, column=0, sticky='news') # onde o botão deve aparecer
      btn_eq.grid(row=0, column=1, sticky='news')

      self.style.configure('Result.TButton', font=fontConfig)

      frame.columnconfigure(0, weight=1)
      frame.columnconfigure(1, weight=1)
      frame.rowconfigure(0, weight=1)
  #END def _BuildBottomFrameContent

  # Método que limpa a entry, e insere 0 como argumento padrão
  # Com a nova modificação da Entry
  def _btn_clr_action(self): 
      self.entry_display.delete(0,'end')
      self.entry_display.insert(END,'0')
      self.currentNumber = '0'
  # END def _btn_clr_action(self):

  # Método que apaga o último elemento da expressão
  # Baseado na função acima, apenas se diferenciando na remoção de apenas um elemento da expressão  
  def _btn_clr_last_action(self, event=None): 
      currentValues = self.entry_display.get()[:-1]
      self.entry_display.delete(0, 'end')
      self.entry_display.insert(END, currentValues)
      self.currentNumber = currentValues
    
  # Método que calcula o resultado da expressão digitada.
  # Inicialmente é instânciado o objeto expTree da classe ExpressionTree, utilizando o método _BuildExpressionTree
  # logo após e invocado o método calc do objeto expTree, para calcular a expressão construida na árvore.
  # Este método retorna o resultado na expressão, onde a mesma é inserida no display, caso não exista problemas
  # de divisão com zero.
  def _btn_eq_action(self, event = None): # Método que o botão "=" e a tecla enter, utilizam como comando
     expTree = self._BuildExpressionTree()
     try:
        result = str(expTree.calc())
     except ZeroDivisionError:
        result = 'Division Error'

     self.entry_display.delete(0,'end')
     self.entry_display.insert(END, result)
     self.currentNumber = '0'  # Reinicia para permitir a inserção de um novo número

     if not result.isnumeric() and result != 'Division Error':
        self.currentNumber = result

# END def _btn_eq_action(self):

  # Constrói a árvore de expressão, instânciando o objeto expTree da classe ExpressionTree
  # Pega a expressão do display e verifica se é uma expressão válida e trata ela.
  # Foi melhorado essa construção levando em conta que o . é um digito nas operações de ponto flutuante
  # sendo assim é necessário verificar esse digito
  def _BuildExpressionTree(self):
      expTree = ExpressionTree(self.OPERATORS_LEVEL)

      #Obter os numeros e os operadores para
      # adicionar à árvore
      displayExp = self.entry_display.get()
      # exemplo: 78x21/23+ #(Evitar terminar com simbolo)
      if not displayExp[-1].isdigit():
          displayExp = displayExp[:-1]
      # exemplo: 78x2+1/23

      numberStr = ''
      for char  in displayExp:

          if char.isdigit() or char == '.':
            numberStr +=char
          else:
            expTree.add(numberStr)
            numberStr = ''

            expTree.add(char)
      #END for char
      expTree.add(numberStr)

      return expTree

  #END def _BuildExpressionTree
# END class Calculadora

Calculadora()# Criar um objeto de tipo calculadora


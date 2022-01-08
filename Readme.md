# Predicción de valores y gestión de cartera en el mercado bursátil - JorgeSaNel
La inversión es la utilización de los recursos en el sector productivo o de capitales cuyo objetivo es lograr beneficios o ganancias en el corto, medio o largo plazo. Su importancia radica en lograr obtener libertad financiera, siendo el principal objetivo de la inversión obtener, al menos, una rentabilidad que consiga suplir la subida anual del IPC español y que, por ende el dinero no se devalúe en el banco. Este proyecto propone el mejor algoritmo para invertir basado en Machine Learning o Deep Learning, pudiendo tomar decisiones algorítmicas y de manera objetiva sin dejarse llevar por sentimientos, los cuales, sin una estrategia clara, vienen a ser como jugar al azar en el casino. Para ello, se extraerán los datos históricos (precio de la acción, volúmen o media de las últimas semanas, entre otros) de las empresas tecnológicas que capitalizan en el mercado americano NASDAQ (National Association of Securities Dealers Automated Quotation), el segundo mercado más grande de los Estados Unidos. Para maximizar los resultados del algoritmo, también se tendrán en cuenta las noticias y eventos del día a día, así como los comentarios subjetivos que proporciona cada inversor de las empresas en las diferentes páginas webs. Juntando todo ello, y tras aplicar el algoritmo, se llegará a los tres escenarios posibles, categorizados como "compra", "venta", o "apalancamiento". Este escenario corresponde a una recomendación de compra/venta, pero depende del perfil del inversor tomar la decisión final.

## Desarrollo
Durante el desarrollo de este proyecto se han logrado los siguientes productos:
•	Desarrollo del código en Google Colab con la predicción diaria de las empresas del SP500. Se ha utilizado el algoritmo LSTM  (Long-Short Term Memory), obteniendo una precisión media del 95% para más de 300 empresas. Para las empresas restantes, la precisión ronda entre 80% y 95%.
•	Se ha comparado el algoritmo LSTM con el algortimo ARIMA, llegando a la conclusión de que este último no es bueno para predicciones ya que no tiene estacionalidad.
•	Se ha conectado el código con Gsheets para poder tener una interfaz de usuario.
•	Gracias al Excel, se ha podido realizar una gestión de cartera para alertar al inversor de posibles tendencias alcistas o bajistas en base a las métricas utilizadas (EMA10, SMA20, SMA50, SMA100 y SMA200) y a los valores de los analistas.


## Author
Jorge Santos Neila
email: `jorgesantosneila@gmail.com`
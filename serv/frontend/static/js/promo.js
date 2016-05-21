var round = Math.round;
var i = 0;

var CColor = (typeof CColor === 'undefined') ? "#fff" : CColor; //Цвет стрелок
var CBackground = (typeof CBackground === 'undefined') ? "#2980b9" : CBackground; //Цвет фона
var CSeconds = (typeof CSeconds === 'undefined') ? "#f37019" : CSeconds; //Цвет секундной стрелки
var CSize = 280; //Размер поля
var CCenter = CSize / 2; //Радиус круга
var CTSize = CCenter - 10; //Расстояние от центра где рисуются отметки минут
var CMSize = CTSize * 0.9; //Длинна минутной стрелки
var CSSize = CTSize * 0.8; //Длинна секундной стрелки
var CHSize = CTSize * 0.6; //Длинна часовой стрелки
var example;

function ctxline(x1,y1,len,angle,color,wid){//Функция рисования линии под углом
    var x2 = (CCenter + (len * Math.cos(angle)));
    var y2 = (CCenter + (len * Math.sin(angle)));
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = wid;
    ctx.moveTo(x1,y1);
    ctx.lineTo(x2,y2);
    ctx.stroke();
}

function ctxcircle(x,y,rd,color){//Функция рисования круга
    ctx.beginPath();
    ctx.arc(x, y, rd, 0, 2*Math.PI, false);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.lineWidth = 1;
    ctx.strokeStyle = color;
    ctx.stroke();
}

function tick(diff){ //Функция рисования стрелок
    //Стираем предыдущие стрелки
    var TTimeDiff = (typeof diff === 'undefined') ? 0 : round(diff); 

    ctxcircle(CCenter, CCenter, CTSize, CBackground);
    //Вычисляем поворот
    i = 360/3600 * ((new Date().getMinutes()*60)+new Date().getSeconds() + TTimeDiff) 

    //Рисуем стрелку
    ctxline(CCenter,CCenter,CMSize,((i-90) / 180 * Math.PI),CColor,4);//Минутная

    i = 360/720*( (new Date().getHours()*60)+ new Date().getMinutes() + TTimeDiff/60);
    ctxline(CCenter,CCenter,CHSize,((i-90) / 180 * Math.PI),CColor,5)// Часовая

    ctxcircle(CCenter,CCenter,9,CColor);//Круг от стрелки

    //i = 360/(60*1000)* ((new Date().getSeconds()*1000)+ new Date().getMilliseconds());
    //ctxline(CCenter,CCenter,CSSize,((i-90) / 180 * Math.PI),CSeconds,3);//Секундная

    ctxcircle(CCenter,CCenter,6,CSeconds);//Круг от секундной стрелки
}

function loadClock(id, diff) 
{
    
    if (typeof window.intervalId !== 'undefined') {
        clearInterval(window.intervalId);
    }

    example= document.getElementById(id), ctx = example.getContext('2d');
    ctx.fillStyle = CBackground;
    ctx.fillRect(0, 0,example.width,example.height);


    ctx.beginPath();
    ctx.arc(CCenter,CCenter, CTSize, 0, 2*Math.PI, false);

    ctx.lineWidth = 10;
    ctx.strokeStyle = CColor;
    ctx.stroke();

    
    window.intervalId = setInterval(function() { tick(diff);} ,10);
    
}

function loadTime(id, diff) 
{
    var newDateObj = new Date();
    newDateObj.setTime(newDateObj.getTime() + (diff * 1000));
    $('#'+id).html(newDateObj.toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'})); 
}




function getDate() {
    var today = new Date();
    // var date = today.getFullYear() + "-" + twoDigits(today.getMonth() + 1) + "-" + twoDigits(today.getDate()) + " ";
    var date = twoDigits(today.getFullYear()) + "-" + twoDigits(today.getMonth() + 1) + "-" + twoDigits(today.getDate()) + " ";
    var week = " 星期" + "日一二三四五六 ".charAt(today.getDay()) + " ";
    var time = twoDigits(today.getHours()) + ": " + twoDigits(today.getMinutes()) + ": " + twoDigits(today.getSeconds()) + " ";
    $(".time").html(date + week +time);
}
function twoDigits(val) {
    if (val < 10) return "0" + val; return val;
}

$(function () {
    setInterval(getDate, 1000);
});
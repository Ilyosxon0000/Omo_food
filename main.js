// let interval = setInterval(
//     () => {
//         console.log("interval");
//     },1000
// )
// // console.log("out interval");
// clearInterval(interval)
// let diffTime = Math.abs(new Date().valueOf() - new Date('2021-11-22T18:30:00').valueOf());
// console.log(diffTime);

let backend_seconds = 2589556.309874;
let diffTime = backend_seconds*1000;
let days = diffTime / (24*60*60*1000);
let hours = (days % 1) * 24;
let minutes = (hours % 1) * 60;
let secs = (minutes % 1) * 60;
[days, hours, minutes, secs] = [Math.floor(days), Math.floor(hours), Math.floor(minutes), Math.floor(secs)]

console.log(days+'d', hours+'h', minutes+'m', secs+'s');
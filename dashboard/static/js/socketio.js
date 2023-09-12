//./static/js/style.js
document.addEventListener('DOMContentLoaded', function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    socket.on('connect', function() {
        console.log('Connected to WebSocket');
    });

    socket.on('update_ultrasonic', function(data) {
        console.log('Ultrasonic Data:', data);
        updateUltrasonicValues(data);
    });

    socket.on('update_mpu6050', function(data) {
        console.log('MPU6050 Data:', data);
        updateMPU6050Values(data);
    });

    function updateUltrasonicValues(data) {
        document.getElementById('ultrasonic-left').textContent = data.left;
        document.getElementById('ultrasonic-central').textContent = data.central;
        document.getElementById('ultrasonic-right').textContent = data.right;
    }

    function updateMPU6050Values(data) {
        document.getElementById('mpu6050-acceleration-x').textContent = data.acceleration_x;
        document.getElementById('mpu6050-acceleration-y').textContent = data.acceleration_y;
        document.getElementById('mpu6050-acceleration-z').textContent = data.acceleration_z;
        document.getElementById('mpu6050-gyro-x').textContent = data.gyro_x;
        document.getElementById('mpu6050-gyro-y').textContent = data.gyro_y;
        document.getElementById('mpu6050-gyro-z').textContent = data.gyro_z;
        document.getElementById('mpu6050-temperature').textContent = data.temperature;
    }
});

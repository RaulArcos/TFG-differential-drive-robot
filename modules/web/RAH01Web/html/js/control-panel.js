var status = 0

document.getElementById('toggleIconBtn').addEventListener('click', function() {
    var icon = this.querySelector('i');
    var buttonMenu = document.getElementById('button-menu');
    var joystickMenu = document.getElementById('joystick-menu');

    // Toggle icon and menus
    if (status==0) {
        icon.classList.remove('fa-solid', 'fa-microchip');
        icon.classList.add('fa-solid', 'fa-gamepad');
        buttonMenu.style.display = 'none';
        joystickMenu.style.display = 'block'; // Show joystick menu
        status+=1;
    } else {
        icon.classList.remove('fa-solid', 'fa-gamepad');
        icon.classList.add('fa-solid', 'fa-microchip');
        buttonMenu.style.display = 'block';
        joystickMenu.style.display = 'none'; // Hide joystick menu
        status-=1;
    }
});
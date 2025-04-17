document.addEventListener("DOMContentLoaded", function() {
            const line = document.getElementById('animatedLine');
            let movingRight = true;
            let dashCount = 0;

            function updateLine() {
                if (movingRight) {
                    dashCount++;
                } else {
                    dashCount--;
                }

                // Create dashes based on the dashCount with different colors
                const dashes = Array.from({length: dashCount}, (_, i) => {
                    const color = `hsl(${(i * 36) % 360}, 100%, 50%)`; // Generates a different hue for each dash
                    return `<span style="color: ${color}; text-shadow: 0 0 5px ${color}, 0 0 10px ${color};">-</span>`;
                }).join('');
                
                line.innerHTML = movingRight ? `${dashes} <span style="color:#00ff00;">&gt;</span>` : `<span style="color:#00ff00;">&lt;</span> ${dashes}`;

                // Change direction when dashes reach a limit
                if (dashCount >= 10) { // Maximum da=sh count
                    movingRight = false;
                } else if (dashCount <= 0) { // Minimum dash count
                    movingRight = true;
                 }
            }

            // Update the line every 100 milliseconds
            setInterval(updateLine, 300);
        });

        function togglePassword() {
            const passwordInput = document.getElementById('password');
            passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
        }
        
        
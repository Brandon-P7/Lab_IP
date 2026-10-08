from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Roguelite Geométrico - Flask Edition</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0f0f19; color: #fff; font-family: system-ui, sans-serif; overflow: hidden; }
        canvas { background: radial-gradient(circle, #1a1a2e 0%, #0f0f19 100%); box-shadow: 0 0 30px rgba(0,255,128,0.1); }
    </style>
</head>
<body class="flex flex-col items-center justify-center h-screen select-none">

    <!-- CONTENEDOR DEL JUEGO -->
    <div id="game-container" class="relative shadow-2xl rounded-xl border border-gray-800">
        <canvas id="gameCanvas" width="900" height="600" class="rounded-xl cursor-crosshair"></canvas>
        
        <!-- MENÚ PRINCIPAL -->
        <div id="menu-screen" class="absolute inset-0 bg-[#0f0f19]/90 backdrop-blur-sm flex flex-col items-center justify-center space-y-6">
            <h1 class="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 tracking-wider">ROGUELITE GEOMÉTRICO</h1>
            <p class="text-gray-400 text-lg">Sobrevive a las rondas, recolecta monedas amarillas y enfréntate a Jefes aleatorios.</p>
            <div class="flex flex-col gap-3 w-64">
                <button onclick="startGame()" class="bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-bold py-3 px-6 rounded-lg shadow-lg transition transform hover:scale-105">JUGAR PARTIDA</button>
            </div>
            <div class="text-xs text-gray-500 mt-4">Controles: WASD mover | Clic o ESPACIO para disparar hacia el cursor</div>
        </div>

        <!-- PANTALLA DE TIENDA -->
        <div id="shop-screen" class="absolute inset-0 bg-gray-950/95 backdrop-blur-md flex flex-col items-center justify-center space-y-6 hidden">
            <h2 id="shop-title" class="text-4xl font-bold text-yellow-400 tracking-wide">TIENDA DE MEJORAS</h2>
            <p id="shop-credits" class="text-xl text-emerald-400 font-semibold">Monedas: ¢0</p>
            <div class="flex flex-col gap-3 w-96">
                <button onclick="buyUpgrade('damage')" class="bg-gray-800 hover:bg-gray-700 border border-yellow-500/30 p-3 rounded-xl flex justify-between items-center transition">
                    <span>⚡ Aumentar Daño (+1)</span>
                    <span class="text-yellow-400 font-bold">¢50</span>
                </button>
                <button onclick="buyUpgrade('speed')" class="bg-gray-800 hover:bg-gray-700 border border-yellow-500/30 p-3 rounded-xl flex justify-between items-center transition">
                    <span>👢 Aumentar Velocidad</span>
                    <span class="text-yellow-400 font-bold">¢40</span>
                </button>
                <button onclick="buyUpgrade('life')" class="bg-gray-800 hover:bg-gray-700 border border-yellow-500/30 p-3 rounded-xl flex justify-between items-center transition">
                    <span>❤️ Vida Extra (+1 Máxima)</span>
                    <span class="text-yellow-400 font-bold">¢80</span>
                </button>
                <button onclick="buyUpgrade('laser')" class="bg-gray-800 hover:bg-gray-700 border border-yellow-500/30 p-3 rounded-xl flex justify-between items-center transition">
                    <span>🌀 Potenciar Rayo de Ataque</span>
                    <span class="text-yellow-400 font-bold">¢100</span>
                </button>
            </div>
            <button onclick="nextRound()" class="mt-2 bg-yellow-500 hover:bg-yellow-400 text-gray-950 font-bold py-3 px-8 rounded-lg shadow-lg transition transform hover:scale-105">SIGUIENTE RONDA ➔</button>
        </div>

        <!-- PANTALLA DE GAME OVER / VICTORIA -->
        <div id="end-screen" class="absolute inset-0 bg-black/90 flex flex-col items-center justify-center space-y-6 hidden">
            <h2 id="end-title" class="text-5xl font-extrabold text-red-500">¡HAS MUERTO!</h2>
            <p id="end-score" class="text-xl text-gray-300">Puntuación final: 0</p>
            <button onclick="resetGame()" class="bg-cyan-500 hover:bg-cyan-400 text-gray-950 font-bold py-3 px-6 rounded-lg transition">MENÚ PRINCIPAL</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let gameState = "MENU"; // MENU, PLAYING, SHOP, END
        let score = 0, credits = 0, round = 1, maxRounds = 10;
        let enemiesToSpawn = 0, spawnTimer = 0;

        let player = {
            x: canvas.width / 2,
            y: canvas.height / 2,
            radius: 16,
            speed: 4,
            maxLife: 3,
            life: 3,
            damage: 1,
            laserPower: 1,
            cadence: 200,
            lastShot: 0
        };

        let keys = {};
        let mouse = { x: canvas.width/2, y: canvas.height/2, down: false };
        let bullets = [];
        let enemies = [];
        let coins = [];

        window.addEventListener("keydown", e => {
            keys[e.key.toLowerCase()] = true;
            if (e.code === "Space") {
                mouse.down = true;
                e.preventDefault();
            }
        });
        window.addEventListener("keyup", e => {
            keys[e.key.toLowerCase()] = false;
            if (e.code === "Space") {
                mouse.down = false;
            }
        });
        canvas.addEventListener("mousemove", e => {
            const rect = canvas.getBoundingClientRect();
            mouse.x = e.clientX - rect.left;
            mouse.y = e.clientY - rect.top;
        });
        canvas.addEventListener("mousedown", () => mouse.down = true);
        canvas.addEventListener("mouseup", () => mouse.down = false);

        function startGame() {
            document.getElementById("menu-screen").classList.add("hidden");
            
            // REINICIO COMPLETO DE ESTADÍSTICAS
            player.x = canvas.width / 2;
            player.y = canvas.height / 2;
            player.speed = 4;
            player.maxLife = 3;
            player.life = 3;
            player.damage = 1;
            player.laserPower = 1;
            
            score = 0;
            credits = 0;
            round = 1;
            initRound();
            gameState = "PLAYING";
        }

        function initRound() {
            bullets = [];
            enemies = [];
            coins = [];
            enemiesToSpawn = 6 + (round * 4);
            spawnTimer = 0;

            // Probabilidad aleatoria de aparición de jefe al iniciar ronda (35% de probabilidad a partir de ronda 2)
            if (round >= 2 && Math.random() < 0.35) {
                spawnBoss();
            }
        }

        function spawnBoss() {
            let edge = Math.floor(Math.random() * 4);
            let ex, ey;
            if (edge === 0) { ex = Math.random() * canvas.width; ey = -40; }
            else if (edge === 1) { ex = Math.random() * canvas.width; ey = canvas.height + 40; }
            else if (edge === 2) { ex = -40; ey = Math.random() * canvas.height; }
            else { ex = canvas.width + 40; ey = Math.random() * canvas.height; }

            enemies.push({
                x: ex, y: ey,
                type: "boss",
                hp: 15 + (round * 5),
                radius: 32,
                speed: 1.2,
                reward: 100,
                color: "#ff0055"
            });
        }

        function buyUpgrade(type) {
            if (type === 'damage' && credits >= 50) { credits -= 50; player.damage += 1; }
            else if (type === 'speed' && credits >= 40) { credits -= 40; player.speed += 0.8; }
            else if (type === 'life' && credits >= 80) { credits -= 80; player.maxLife += 1; player.life = player.maxLife; }
            else if (type === 'laser' && credits >= 100) { credits -= 100; player.laserPower += 1; }
            document.getElementById("shop-credits").innerText = `Monedas: ¢${credits}`;
        }

        function nextRound() {
            round++;
            if (round > maxRounds) {
                endGame(true);
            } else {
                document.getElementById("shop-screen").classList.add("hidden");
                initRound();
                gameState = "PLAYING";
            }
        }

        function endGame(victory) {
            gameState = "END";
            document.getElementById("shop-screen").classList.add("hidden");
            const titleEl = document.getElementById("end-title");
            titleEl.innerText = victory ? "¡VICTORIA ÉPICA!" : "¡HAS MUERTO!";
            titleEl.className = victory ? "text-5xl font-extrabold text-emerald-400" : "text-5xl font-extrabold text-red-500";
            document.getElementById("end-score").innerText = `Puntuación obtenida: ${score}`;
            document.getElementById("end-screen").classList.remove("hidden");
        }

        function resetGame() {
            document.getElementById("end-screen").classList.add("hidden");
            document.getElementById("menu-screen").classList.remove("hidden");
            gameState = "MENU";
        }

        // Bucle Principal del Juego
        function update() {
            if (gameState !== "PLAYING") return;

            // Movimiento del jugador
            if (keys['w'] || keys['arrowup']) player.y -= player.speed;
            if (keys['s'] || keys['arrowdown']) player.y += player.speed;
            if (keys['a'] || keys['arrowleft']) player.x -= player.speed;
            if (keys['d'] || keys['arrowright']) player.x += player.speed;

            player.x = Math.max(player.radius, Math.min(canvas.width - player.radius, player.x));
            player.y = Math.max(player.radius, Math.min(canvas.height - player.radius, player.y));

            // Disparos (Clic o Espacio hacia el puntero del mouse)
            if (mouse.down) {
                let now = Date.now();
                if (now - player.lastShot > player.cadence) {
                    let angle = Math.atan2(mouse.y - player.y, mouse.x - player.x);
                    
                    // Capacidad de rayo potenciado (dispara múltiples proyectiles en abanico según laserPower)
                    let count = player.laserPower;
                    let spread = 0.15;
                    for (let i = 0; i < count; i++) {
                        let offsetAngle = angle + (i - (count - 1) / 2) * spread;
                        bullets.push({
                            x: player.x, y: player.y,
                            dx: Math.cos(offsetAngle) * 10, dy: Math.sin(offsetAngle) * 10,
                            damage: player.damage, radius: 4 + (player.laserPower * 0.5)
                        });
                    }
                    player.lastShot = now;
                }
            }

            // Generación de enemigos rojos regulares
            if (enemiesToSpawn > 0) {
                spawnTimer++;
                if (spawnTimer > Math.max(20, 50 - (round * 2))) {
                    let edge = Math.floor(Math.random() * 4);
                    let ex, ey;
                    if (edge === 0) { ex = Math.random() * canvas.width; ey = -20; }
                    else if (edge === 1) { ex = Math.random() * canvas.width; ey = canvas.height + 20; }
                    else if (edge === 2) { ex = -20; ey = Math.random() * canvas.height; }
                    else { ex = canvas.width + 20; ey = Math.random() * canvas.height; }

                    enemies.push({
                        x: ex, y: ey,
                        type: "normal",
                        hp: 1 + Math.floor(round / 3),
                        radius: 14,
                        speed: 2 + (round * 0.08),
                        reward: 10,
                        color: "#ef4444" // Color rojo solicitado
                    });
                    enemiesToSpawn--;
                    spawnTimer = 0;
                }
            }

            // Actualizar Balas
            for (let i = bullets.length - 1; i >= 0; i--) {
                let b = bullets[i];
                b.x += b.dx; b.y += b.dy;
                if (b.x < 0 || b.x > canvas.width || b.y < 0 || b.y > canvas.height) {
                    bullets.splice(i, 1);
                }
            }

            // Actualizar Monedas (Desaparecen a los 5 segundos / 300 frames)
            for (let i = coins.length - 1; i >= 0; i--) {
                coins[i].timer--;
                if (coins[i].timer <= 0) {
                    coins.splice(i, 1);
                    continue;
                }
                // Colisión con jugador para recoger moneda
                let dist = Math.hypot(player.x - coins[i].x, player.y - coins[i].y);
                if (dist < player.radius + coins[i].radius) {
                    credits += coins[i].value;
                    score += coins[i].value;
                    coins.splice(i, 1);
                }
            }

            // Actualizar Enemigos y Colisiones
            for (let i = enemies.length - 1; i >= 0; i--) {
                let e = enemies[i];
                let angle = Math.atan2(player.y - e.y, player.x - e.x);
                e.x += Math.cos(angle) * e.speed;
                e.y += Math.sin(angle) * e.speed;

                // Colisión con Jugador (El enemigo rojo toca al jugador)
                let distPlayer = Math.hypot(player.x - e.x, player.y - e.y);
                if (distPlayer < player.radius + e.radius) {
                    player.life--;
                    enemies.splice(i, 1);
                    if (player.life <= 0) {
                        endGame(false);
                    }
                    continue;
                }

                // Colisión con Balas
                for (let j = bullets.length - 1; j >= 0; j--) {
                    let b = bullets[j];
                    let distBullet = Math.hypot(b.x - e.x, b.y - e.y);
                    if (distBullet < b.radius + e.radius) {
                        e.hp -= b.damage;
                        bullets.splice(j, 1);
                        if (e.hp <= 0) {
                            // Al morir el enemigo, genera moneda amarilla que dura 5 segundos (300 frames)
                            coins.push({
                                x: e.x, y: e.y,
                                radius: 10,
                                value: e.reward,
                                timer: 300 
                            });
                            enemies.splice(i, 1);
                            break;
                        }
                    }
                }
            }

            // Verificar fin de ronda
            if (enemiesToSpawn === 0 && enemies.length === 0) {
                if (round >= maxRounds) {
                    endGame(true);
                } else {
                    document.getElementById("shop-credits").innerText = `Monedas: ¢${credits}`;
                    document.getElementById("shop-screen").classList.remove("hidden");
                    gameState = "SHOP";
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Rejilla de fondo estilo arena
            ctx.strokeStyle = "#1e1e30";
            ctx.lineWidth = 1;
            for (let x = 0; x < canvas.width; x += 40) {
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
            }
            for (let y = 0; y < canvas.height; y += 40) {
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
            }

            if (gameState === "PLAYING") {
                // Dibujar Monedas Amarillas (parpadean si les queda poco tiempo)
                for (let c of coins) {
                    ctx.fillStyle = c.timer < 90 && Math.floor(c.timer / 10) % 2 === 0 ? "#fff" : "#facc15";
                    ctx.beginPath(); ctx.arc(c.x, c.y, c.radius, 0, Math.PI * 2); ctx.fill();
                    ctx.strokeStyle = "#ca8a04"; ctx.lineWidth = 2; ctx.stroke();
                }

                // Dibujar Jugador
                ctx.fillStyle = "#3b82f6";
                ctx.beginPath(); ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2); ctx.fill();
                ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.stroke();

                // Dibujar Balas
                ctx.fillStyle = "#10b981";
                for (let b of bullets) {
                    ctx.beginPath(); ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2); ctx.fill();
                }

                // Dibujar Enemigos (Rojos)
                for (let e of enemies) {
                    ctx.fillStyle = e.color;
                    ctx.beginPath(); ctx.arc(e.x, e.y, e.radius, 0, Math.PI * 2); ctx.fill();
                    ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.stroke();
                }

                // HUD en pantalla
                ctx.fillStyle = "#fff";
                ctx.font = "bold 16px sans-serif";
                ctx.fillText(`Ronda: ${round}/${maxRounds} | Vidas: ${'❤️ '.repeat(player.life)} | Monedas: ¢${credits} | Restantes: ${enemiesToSpawn + enemies.length}`, 20, 30);
            }
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    print("Iniciando servidor de Flask... Abre http://127.0.0.1:5000 en tu navegador.")
    app.run(debug=True)
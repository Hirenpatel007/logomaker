/**
 * 3D Components for LogoMaker Pro
 * Created by Hiren Patel
 */

class LogoMaker3D {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.logoMeshes = [];
        this.particles = [];
        this.animationId = null;
        this.isInitialized = false;
    }

    // Initialize 3D Scene
    init(containerId) {
        try {
            const container = document.getElementById(containerId);
            if (!container) {
                console.error('Container not found:', containerId);
                return false;
            }

            // Scene setup
            this.scene = new THREE.Scene();
            this.scene.fog = new THREE.Fog(0x050505, 1, 1000);

            // Camera setup
            this.camera = new THREE.PerspectiveCamera(
                75,
                container.offsetWidth / container.offsetHeight,
                0.1,
                1000
            );
            this.camera.position.z = 30;

            // Renderer setup
            this.renderer = new THREE.WebGLRenderer({ 
                alpha: true, 
                antialias: true 
            });
            this.renderer.setSize(container.offsetWidth, container.offsetHeight);
            this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            this.renderer.setClearColor(0x000000, 0);
            container.appendChild(this.renderer.domElement);

            // Add lighting
            this.setupLighting();

            // Create floating logos
            this.createFloatingLogos();

            // Create particle system
            this.createParticleSystem();

            // Start animation
            this.animate();

            // Handle resize
            this.setupResize(container);

            this.isInitialized = true;
            return true;
        } catch (error) {
            console.error('Failed to initialize 3D scene:', error);
            return false;
        }
    }

    // Setup lighting
    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
        this.scene.add(ambientLight);

        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(50, 50, 50);
        directionalLight.castShadow = true;
        this.scene.add(directionalLight);

        // Point lights for colorful effects
        const colors = [0x3b82f6, 0x8b5cf6, 0xf59e0b, 0xef4444];
        colors.forEach((color, index) => {
            const light = new THREE.PointLight(color, 0.5, 100);
            light.position.set(
                Math.sin(index * Math.PI / 2) * 30,
                Math.cos(index * Math.PI / 2) * 30,
                10
            );
            this.scene.add(light);
        });
    }

    // Create floating logo shapes
    createFloatingLogos() {
        const logoShapes = [
            // Cube logo
            {
                geometry: new THREE.BoxGeometry(2, 2, 2),
                material: new THREE.MeshPhongMaterial({ 
                    color: 0x3b82f6,
                    transparent: true,
                    opacity: 0.8,
                    wireframe: false
                }),
                position: { x: -15, y: 5, z: -10 },
                rotation: { x: 0, y: 0, z: 0 }
            },
            // Sphere logo
            {
                geometry: new THREE.SphereGeometry(1.5, 32, 32),
                material: new THREE.MeshPhongMaterial({ 
                    color: 0x8b5cf6,
                    transparent: true,
                    opacity: 0.8,
                    wireframe: false
                }),
                position: { x: 10, y: -3, z: -5 },
                rotation: { x: 0, y: 0, z: 0 }
            },
            // Torus logo
            {
                geometry: new THREE.TorusGeometry(1.5, 0.5, 16, 100),
                material: new THREE.MeshPhongMaterial({ 
                    color: 0xf59e0b,
                    transparent: true,
                    opacity: 0.8,
                    wireframe: false
                }),
                position: { x: 0, y: 8, z: -15 },
                rotation: { x: 0, y: 0, z: 0 }
            },
            // Octahedron logo
            {
                geometry: new THREE.OctahedronGeometry(2),
                material: new THREE.MeshPhongMaterial({ 
                    color: 0xef4444,
                    transparent: true,
                    opacity: 0.8,
                    wireframe: false
                }),
                position: { x: -8, y: -5, z: -8 },
                rotation: { x: 0, y: 0, z: 0 }
            }
        ];

        logoShapes.forEach((shape, index) => {
            const mesh = new THREE.Mesh(shape.geometry, shape.material);
            mesh.position.set(shape.position.x, shape.position.y, shape.position.z);
            mesh.userData = {
                originalPosition: { ...shape.position },
                rotationSpeed: {
                    x: (Math.random() - 0.5) * 0.02,
                    y: (Math.random() - 0.5) * 0.02,
                    z: (Math.random() - 0.5) * 0.02
                },
                floatSpeed: Math.random() * 0.005 + 0.002,
                floatRange: Math.random() * 2 + 1
            };
            this.logoMeshes.push(mesh);
            this.scene.add(mesh);
        });
    }

    // Create particle system
    createParticleSystem() {
        const particleCount = 1000;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 100;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 100;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 100;

            const color = new THREE.Color();
            color.setHSL(Math.random(), 0.7, 0.6);
            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 0.5,
            vertexColors: true,
            transparent: true,
            opacity: 0.6
        });

        const particles = new THREE.Points(geometry, material);
        this.particles.push(particles);
        this.scene.add(particles);
    }

    // Animation loop
    animate() {
        if (!this.isInitialized) return;

        this.animationId = requestAnimationFrame(() => this.animate());

        const time = Date.now() * 0.001;

        // Animate floating logos
        this.logoMeshes.forEach((mesh, index) => {
            // Rotation
            mesh.rotation.x += mesh.userData.rotationSpeed.x;
            mesh.rotation.y += mesh.userData.rotationSpeed.y;
            mesh.rotation.z += mesh.userData.rotationSpeed.z;

            // Floating motion
            mesh.position.y = mesh.userData.originalPosition.y + 
                Math.sin(time * mesh.userData.floatSpeed + index) * mesh.userData.floatRange;
        });

        // Animate particles
        this.particles.forEach(particle => {
            particle.rotation.x += 0.001;
            particle.rotation.y += 0.002;
        });

        // Camera subtle movement
        this.camera.position.x = Math.sin(time * 0.1) * 2;
        this.camera.position.y = Math.cos(time * 0.15) * 1;
        this.camera.lookAt(this.scene.position);

        this.renderer.render(this.scene, this.camera);
    }

    // Handle window resize
    setupResize(container) {
        window.addEventListener('resize', () => {
            if (!this.isInitialized) return;

            this.camera.aspect = container.offsetWidth / container.offsetHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(container.offsetWidth, container.offsetHeight);
        });
    }

    // Cleanup
    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        if (this.renderer) {
            this.renderer.dispose();
        }
        
        this.logoMeshes.forEach(mesh => {
            mesh.geometry.dispose();
            mesh.material.dispose();
        });

        this.particles.forEach(particle => {
            particle.geometry.dispose();
            particle.material.dispose();
        });

        this.isInitialized = false;
    }
}

// Logo Preview 3D Component
class LogoPreview3D {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.logoPlane = null;
        this.animationId = null;
    }

    init(containerId, logoUrl) {
        const container = document.getElementById(containerId);
        if (!container) return false;

        // Scene setup
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
        this.camera.position.z = 5;

        // Renderer setup
        this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        this.renderer.setSize(300, 300);
        this.renderer.setClearColor(0x000000, 0);
        container.appendChild(this.renderer.domElement);

        // Load logo texture
        if (logoUrl) {
            this.loadLogoTexture(logoUrl);
        }

        // Add lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(1, 1, 1);
        this.scene.add(directionalLight);

        this.animate();
        return true;
    }

    loadLogoTexture(url) {
        const textureLoader = new THREE.TextureLoader();
        textureLoader.load(url, (texture) => {
            const geometry = new THREE.PlaneGeometry(4, 4);
            const material = new THREE.MeshLambertMaterial({ 
                map: texture,
                transparent: true
            });
            
            if (this.logoPlane) {
                this.scene.remove(this.logoPlane);
            }
            
            this.logoPlane = new THREE.Mesh(geometry, material);
            this.scene.add(this.logoPlane);
        });
    }

    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());

        if (this.logoPlane) {
            this.logoPlane.rotation.y += 0.01;
        }

        this.renderer.render(this.scene, this.camera);
    }

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.renderer) {
            this.renderer.dispose();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize main 3D scene on homepage
    if (document.getElementById('hero-3d-scene')) {
        const logoMaker3D = new LogoMaker3D();
        if (logoMaker3D.init('hero-3d-scene')) {
            console.log('3D Hero scene initialized successfully');
        }
    }

    // Initialize logo preview 3D components
    document.querySelectorAll('.logo-preview-3d').forEach((container, index) => {
        const preview3D = new LogoPreview3D();
        if (preview3D.init(container.id, container.dataset.logoUrl)) {
            console.log(`3D Logo preview ${index} initialized successfully`);
        }
    });
});

// Export classes for global use
window.LogoMaker3D = LogoMaker3D;
window.LogoPreview3D = LogoPreview3D;
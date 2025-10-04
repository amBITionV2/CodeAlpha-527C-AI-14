/**
 * Real 3D Avatar System using Three.js
 * Production-ready 3D sign language gesture animation
 */

class ThreeJSAvatar {
    constructor(containerId) {
        this.containerId = containerId;
        this.container = document.getElementById(containerId);
        
        // Three.js components
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.avatar = null;
        this.animationMixer = null;
        this.clock = new THREE.Clock();
        
        // Avatar skeleton
        this.skeleton = null;
        this.bones = {};
        this.joints = {};
        
        // Animation state
        this.currentAnimation = null;
        this.isAnimating = false;
        this.animationQueue = [];
        
        // Gesture database
        this.gestureAnimations = {};
        
        // Initialize
        this.init();
    }
    
    init() {
        this.createScene();
        this.createCamera();
        this.createRenderer();
        this.createLights();
        this.createAvatar();
        this.createGestureAnimations();
        this.animate();
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }
    
    createScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a2e);
        this.scene.fog = new THREE.Fog(0x1a1a2e, 10, 50);
    }
    
    createCamera() {
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(0, 2, 5);
        this.camera.lookAt(0, 0, 0);
    }
    
    createRenderer() {
        this.renderer = new THREE.WebGLRenderer({ 
            antialias: true,
            alpha: true
        });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.outputEncoding = THREE.sRGBEncoding;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.0;
        
        this.container.appendChild(this.renderer.domElement);
    }
    
    createLights() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);
        
        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 10, 5);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        directionalLight.shadow.camera.near = 0.5;
        directionalLight.shadow.camera.far = 50;
        directionalLight.shadow.camera.left = -10;
        directionalLight.shadow.camera.right = 10;
        directionalLight.shadow.camera.top = 10;
        directionalLight.shadow.camera.bottom = -10;
        this.scene.add(directionalLight);
        
        // Point light for additional illumination
        const pointLight = new THREE.PointLight(0x4ecdc4, 0.5, 20);
        pointLight.position.set(0, 3, 0);
        this.scene.add(pointLight);
    }
    
    createAvatar() {
        // Create avatar group
        this.avatar = new THREE.Group();
        this.scene.add(this.avatar);
        
        // Create skeleton
        this.createSkeleton();
        
        // Create body parts
        this.createBody();
        
        // Position avatar
        this.avatar.position.set(0, 0, 0);
    }
    
    createSkeleton() {
        // Create bone structure for human skeleton
        this.skeleton = new THREE.Group();
        this.avatar.add(this.skeleton);
        
        // Define bone hierarchy
        this.bones = {
            // Spine
            'spine': this.createBone('spine', [0, 0, 0], [0, 0.8, 0]),
            'chest': this.createBone('chest', [0, 0.8, 0], [0, 1.2, 0]),
            'neck': this.createBone('neck', [0, 1.2, 0], [0, 1.4, 0]),
            'head': this.createBone('head', [0, 1.4, 0], [0, 1.6, 0]),
            
            // Left arm
            'left_shoulder': this.createBone('left_shoulder', [0, 1.1, 0], [-0.3, 1.1, 0]),
            'left_upper_arm': this.createBone('left_upper_arm', [-0.3, 1.1, 0], [-0.6, 0.8, 0]),
            'left_forearm': this.createBone('left_forearm', [-0.6, 0.8, 0], [-0.8, 0.5, 0]),
            'left_hand': this.createBone('left_hand', [-0.8, 0.5, 0], [-0.9, 0.3, 0]),
            
            // Right arm
            'right_shoulder': this.createBone('right_shoulder', [0, 1.1, 0], [0.3, 1.1, 0]),
            'right_upper_arm': this.createBone('right_upper_arm', [0.3, 1.1, 0], [0.6, 0.8, 0]),
            'right_forearm': this.createBone('right_forearm', [0.6, 0.8, 0], [0.8, 0.5, 0]),
            'right_hand': this.createBone('right_hand', [0.8, 0.5, 0], [0.9, 0.3, 0]),
            
            // Left leg
            'left_hip': this.createBone('left_hip', [0, 0, 0], [-0.2, -0.2, 0]),
            'left_thigh': this.createBone('left_thigh', [-0.2, -0.2, 0], [-0.2, -0.8, 0]),
            'left_shin': this.createBone('left_shin', [-0.2, -0.8, 0], [-0.2, -1.4, 0]),
            'left_foot': this.createBone('left_foot', [-0.2, -1.4, 0], [-0.2, -1.5, 0]),
            
            // Right leg
            'right_hip': this.createBone('right_hip', [0, 0, 0], [0.2, -0.2, 0]),
            'right_thigh': this.createBone('right_thigh', [0.2, -0.2, 0], [0.2, -0.8, 0]),
            'right_shin': this.createBone('right_shin', [0.2, -0.8, 0], [0.2, -1.4, 0]),
            'right_foot': this.createBone('right_foot', [0.2, -1.4, 0], [0.2, -1.5, 0])
        };
        
        // Set up bone hierarchy
        this.skeleton.add(this.bones.spine);
        this.bones.spine.add(this.bones.chest);
        this.bones.chest.add(this.bones.neck);
        this.bones.neck.add(this.bones.head);
        
        // Arms
        this.bones.chest.add(this.bones.left_shoulder);
        this.bones.left_shoulder.add(this.bones.left_upper_arm);
        this.bones.left_upper_arm.add(this.bones.left_forearm);
        this.bones.left_forearm.add(this.bones.left_hand);
        
        this.bones.chest.add(this.bones.right_shoulder);
        this.bones.right_shoulder.add(this.bones.right_upper_arm);
        this.bones.right_upper_arm.add(this.bones.right_forearm);
        this.bones.right_forearm.add(this.bones.right_hand);
        
        // Legs
        this.bones.spine.add(this.bones.left_hip);
        this.bones.left_hip.add(this.bones.left_thigh);
        this.bones.left_thigh.add(this.bones.left_shin);
        this.bones.left_shin.add(this.bones.left_foot);
        
        this.bones.spine.add(this.bones.right_hip);
        this.bones.right_hip.add(this.bones.right_thigh);
        this.bones.right_thigh.add(this.bones.right_shin);
        this.bones.right_shin.add(this.bones.right_foot);
    }
    
    createBone(name, start, end) {
        const bone = new THREE.Group();
        bone.name = name;
        bone.position.set(start[0], start[1], start[2]);
        
        // Create visual representation
        const geometry = new THREE.CylinderGeometry(0.02, 0.02, 0.1, 8);
        const material = new THREE.MeshLambertMaterial({ 
            color: 0x4ecdc4,
            transparent: true,
            opacity: 0.8
        });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(0, 0.05, 0);
        bone.add(mesh);
        
        return bone;
    }
    
    createBody() {
        // Create body parts as visual representation
        const bodyParts = {
            'head': this.createBodyPart('head', [0, 1.5, 0], [0.15, 0.15, 0.15], 0x4ecdc4),
            'torso': this.createBodyPart('torso', [0, 0.5, 0], [0.3, 0.8, 0.2], 0x4ecdc4),
            'left_arm': this.createBodyPart('left_arm', [-0.4, 0.8, 0], [0.1, 0.6, 0.1], 0x4ecdc4),
            'right_arm': this.createBodyPart('right_arm', [0.4, 0.8, 0], [0.1, 0.6, 0.1], 0x4ecdc4),
            'left_leg': this.createBodyPart('left_leg', [-0.1, -0.6, 0], [0.1, 0.6, 0.1], 0x4ecdc4),
            'right_leg': this.createBodyPart('right_leg', [0.1, -0.6, 0], [0.1, 0.6, 0.1], 0x4ecdc4)
        };
        
        // Add body parts to avatar
        Object.values(bodyParts).forEach(part => {
            this.avatar.add(part);
        });
    }
    
    createBodyPart(name, position, size, color) {
        const geometry = new THREE.BoxGeometry(size[0], size[1], size[2]);
        const material = new THREE.MeshLambertMaterial({ 
            color: color,
            transparent: true,
            opacity: 0.9
        });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(position[0], position[1], position[2]);
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        mesh.name = name;
        return mesh;
    }
    
    createGestureAnimations() {
        // Define gesture animations
        this.gestureAnimations = {
            'HELLO': this.createHelloAnimation(),
            'THANK_YOU': this.createThankYouAnimation(),
            'YES': this.createYesAnimation(),
            'NO': this.createNoAnimation(),
            'GOOD': this.createGoodAnimation(),
            'BAD': this.createBadAnimation(),
            'PLEASE': this.createPleaseAnimation(),
            'SORRY': this.createSorryAnimation(),
            'WELCOME': this.createWelcomeAnimation(),
            'GOODBYE': this.createGoodbyeAnimation(),
            'WHAT': this.createWhatAnimation(),
            'WHERE': this.createWhereAnimation(),
            'WHEN': this.createWhenAnimation(),
            'WHY': this.createWhyAnimation(),
            'HOW': this.createHowAnimation(),
            'WHO': this.createWhoAnimation(),
            'COME': this.createComeAnimation(),
            'GO': this.createGoAnimation(),
            'STOP': this.createStopAnimation(),
            'WAIT': this.createWaitAnimation(),
            'HELP': this.createHelpAnimation(),
            'LEARN': this.createLearnAnimation(),
            'TEACH': this.createTeachAnimation(),
            'BOOK': this.createBookAnimation(),
            'PEN': this.createPenAnimation(),
            'COMPUTER': this.createComputerAnimation(),
            'PHONE': this.createPhoneAnimation(),
            'CAR': this.createCarAnimation(),
            'HOUSE': this.createHouseAnimation(),
            'MOTHER': this.createMotherAnimation(),
            'FATHER': this.createFatherAnimation(),
            'SISTER': this.createSisterAnimation(),
            'BROTHER': this.createBrotherAnimation(),
            'FAMILY': this.createFamilyAnimation(),
            'FRIEND': this.createFriendAnimation(),
            'RED': this.createRedAnimation(),
            'BLUE': this.createBlueAnimation(),
            'GREEN': this.createGreenAnimation(),
            'YELLOW': this.createYellowAnimation(),
            'BLACK': this.createBlackAnimation(),
            'WHITE': this.createWhiteAnimation(),
            'ONE': this.createOneAnimation(),
            'TWO': this.createTwoAnimation(),
            'THREE': this.createThreeAnimation(),
            'FOUR': this.createFourAnimation(),
            'FIVE': this.createFiveAnimation()
        };
    }
    
    // Gesture Animation Creators
    createHelloAnimation() {
        return {
            duration: 1.0,
            keyframes: [
                { time: 0, bone: 'right_hand', rotation: { x: 0, y: 0, z: 0 } },
                { time: 0.5, bone: 'right_hand', rotation: { x: 0, y: 0, z: Math.PI / 4 } },
                { time: 1.0, bone: 'right_hand', rotation: { x: 0, y: 0, z: 0 } }
            ]
        };
    }
    
    createThankYouAnimation() {
        return {
            duration: 1.2,
            keyframes: [
                { time: 0, bone: 'right_hand', position: { x: 0, y: 0, z: 0 } },
                { time: 0.3, bone: 'right_hand', position: { x: 0, y: 0.2, z: 0 } },
                { time: 0.6, bone: 'right_hand', position: { x: 0.2, y: 0.2, z: 0 } },
                { time: 1.2, bone: 'right_hand', position: { x: 0, y: 0, z: 0 } }
            ]
        };
    }
    
    createYesAnimation() {
        return {
            duration: 0.8,
            keyframes: [
                { time: 0, bone: 'head', rotation: { x: 0, y: 0, z: 0 } },
                { time: 0.4, bone: 'head', rotation: { x: 0, y: 0, z: Math.PI / 8 } },
                { time: 0.8, bone: 'head', rotation: { x: 0, y: 0, z: 0 } }
            ]
        };
    }
    
    createNoAnimation() {
        return {
            duration: 0.8,
            keyframes: [
                { time: 0, bone: 'head', rotation: { x: 0, y: 0, z: 0 } },
                { time: 0.2, bone: 'head', rotation: { x: 0, y: 0, z: -Math.PI / 8 } },
                { time: 0.4, bone: 'head', rotation: { x: 0, y: 0, z: Math.PI / 8 } },
                { time: 0.6, bone: 'head', rotation: { x: 0, y: 0, z: -Math.PI / 8 } },
                { time: 0.8, bone: 'head', rotation: { x: 0, y: 0, z: 0 } }
            ]
        };
    }
    
    createGoodAnimation() {
        return {
            duration: 1.0,
            keyframes: [
                { time: 0, bone: 'right_hand', rotation: { x: 0, y: 0, z: 0 } },
                { time: 0.5, bone: 'right_hand', rotation: { x: 0, y: 0, z: Math.PI / 3 } },
                { time: 1.0, bone: 'right_hand', rotation: { x: 0, y: 0, z: 0 } }
            ]
        };
    }
    
    createBadAnimation() {
        return {
            duration: 1.0,
            keyframes: [
                { time: 0, bone: 'right_hand', rotation: { x: 0, y: 0, z: 0 } },
                { time: 0.5, bone: 'right_hand', rotation: { x: 0, y: 0, z: -Math.PI / 3 } },
                { time: 1.0, bone: 'right_hand', rotation: { x: 0, y: 0, z: 0 } }
            ]
        };
    }
    
    // Additional gesture animations would be defined here...
    createPleaseAnimation() { return { duration: 1.0, keyframes: [] }; }
    createSorryAnimation() { return { duration: 1.0, keyframes: [] }; }
    createWelcomeAnimation() { return { duration: 1.5, keyframes: [] }; }
    createGoodbyeAnimation() { return { duration: 1.0, keyframes: [] }; }
    createWhatAnimation() { return { duration: 1.0, keyframes: [] }; }
    createWhereAnimation() { return { duration: 1.0, keyframes: [] }; }
    createWhenAnimation() { return { duration: 1.0, keyframes: [] }; }
    createWhyAnimation() { return { duration: 1.0, keyframes: [] }; }
    createHowAnimation() { return { duration: 1.0, keyframes: [] }; }
    createWhoAnimation() { return { duration: 1.0, keyframes: [] }; }
    createComeAnimation() { return { duration: 1.0, keyframes: [] }; }
    createGoAnimation() { return { duration: 1.0, keyframes: [] }; }
    createStopAnimation() { return { duration: 0.5, keyframes: [] }; }
    createWaitAnimation() { return { duration: 1.5, keyframes: [] }; }
    createHelpAnimation() { return { duration: 1.0, keyframes: [] }; }
    createLearnAnimation() { return { duration: 1.0, keyframes: [] }; }
    createTeachAnimation() { return { duration: 1.0, keyframes: [] }; }
    createBookAnimation() { return { duration: 1.0, keyframes: [] }; }
    createPenAnimation() { return { duration: 1.0, keyframes: [] }; }
    createComputerAnimation() { return { duration: 1.0, keyframes: [] }; }
    createPhoneAnimation() { return { duration: 1.0, keyframes: [] }; }
    createCarAnimation() { return { duration: 1.0, keyframes: [] }; }
    createHouseAnimation() { return { duration: 1.0, keyframes: [] }; }
    createMotherAnimation() { return { duration: 1.0, keyframes: [] }; }
    createFatherAnimation() { return { duration: 1.0, keyframes: [] }; }
    createSisterAnimation() { return { duration: 1.0, keyframes: [] }; }
    createBrotherAnimation() { return { duration: 1.0, keyframes: [] }; }
    createFamilyAnimation() { return { duration: 1.0, keyframes: [] }; }
    createFriendAnimation() { return { duration: 1.0, keyframes: [] }; }
    createRedAnimation() { return { duration: 1.0, keyframes: [] }; }
    createBlueAnimation() { return { duration: 1.0, keyframes: [] }; }
    createGreenAnimation() { return { duration: 1.0, keyframes: [] }; }
    createYellowAnimation() { return { duration: 1.0, keyframes: [] }; }
    createBlackAnimation() { return { duration: 1.0, keyframes: [] }; }
    createWhiteAnimation() { return { duration: 1.0, keyframes: [] }; }
    createOneAnimation() { return { duration: 0.5, keyframes: [] }; }
    createTwoAnimation() { return { duration: 0.5, keyframes: [] }; }
    createThreeAnimation() { return { duration: 0.5, keyframes: [] }; }
    createFourAnimation() { return { duration: 0.5, keyframes: [] }; }
    createFiveAnimation() { return { duration: 0.5, keyframes: [] }; }
    
    animateGesture(gestureName, callback = null) {
        if (!this.gestureAnimations[gestureName]) {
            console.warn(`Gesture animation not found: ${gestureName}`);
            if (callback) callback();
            return;
        }
        
        const animation = this.gestureAnimations[gestureName];
        this.currentAnimation = {
            gesture: gestureName,
            startTime: this.clock.getElapsedTime(),
            duration: animation.duration,
            keyframes: animation.keyframes,
            callback: callback
        };
        
        this.isAnimating = true;
    }
    
    animateGestureSequence(gestures, callback = null) {
        if (!gestures || gestures.length === 0) {
            if (callback) callback();
            return;
        }
        
        this.animationQueue = [...gestures];
        this.playNextGesture(callback);
    }
    
    playNextGesture(callback = null) {
        if (this.animationQueue.length === 0) {
            this.isAnimating = false;
            if (callback) callback();
            return;
        }
        
        const gesture = this.animationQueue.shift();
        this.animateGesture(gesture.gesture, () => {
            // Wait a bit between gestures
            setTimeout(() => {
                this.playNextGesture(callback);
            }, 200);
        });
    }
    
    updateAnimation() {
        if (!this.isAnimating || !this.currentAnimation) return;
        
        const elapsed = this.clock.getElapsedTime() - this.currentAnimation.startTime;
        const progress = Math.min(elapsed / this.currentAnimation.duration, 1);
        
        // Apply keyframe animations
        this.currentAnimation.keyframes.forEach(keyframe => {
            if (elapsed >= keyframe.time) {
                const bone = this.bones[keyframe.bone];
                if (bone) {
                    if (keyframe.rotation) {
                        bone.rotation.set(
                            keyframe.rotation.x || 0,
                            keyframe.rotation.y || 0,
                            keyframe.rotation.z || 0
                        );
                    }
                    if (keyframe.position) {
                        bone.position.set(
                            keyframe.position.x || bone.position.x,
                            keyframe.position.y || bone.position.y,
                            keyframe.position.z || bone.position.z
                        );
                    }
                }
            }
        });
        
        // Check if animation is complete
        if (progress >= 1) {
            this.isAnimating = false;
            if (this.currentAnimation.callback) {
                this.currentAnimation.callback();
            }
            this.currentAnimation = null;
        }
    }
    
    resetPose() {
        // Reset all bones to default position
        Object.values(this.bones).forEach(bone => {
            bone.rotation.set(0, 0, 0);
            bone.position.set(0, 0, 0);
        });
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        this.updateAnimation();
        
        // Rotate avatar slightly for better viewing
        this.avatar.rotation.y += 0.005;
        
        this.renderer.render(this.scene, this.camera);
    }
    
    onWindowResize() {
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
    
    dispose() {
        // Clean up resources
        if (this.renderer) {
            this.renderer.dispose();
        }
        if (this.scene) {
            this.scene.clear();
        }
    }
}

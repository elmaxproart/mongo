<script setup>
import { ref, computed, onBeforeUnmount } from 'vue'
import { 
  Server, Database, Smartphone, User, Image, FileText, ArrowRight, Palette, 
  RefreshCw, Cpu, Layers, HelpCircle, Shield, ShoppingBag, Eye, Tag, 
  Calendar, Key, Play, Pause, RotateCcw, ChevronRight, ChevronLeft, Code 
} from 'lucide-vue-next'

const activeTab = ref('architecture')
const hoveredNode = ref(null)
const selectedCollection = ref('artworks')

// Use cases tab states
const hoveredActor = ref(null)
const activeScenarioId = ref('purchase')
const currentStepIndex = ref(0)
const isPlaying = ref(false)
let playInterval = null

// DB Schema tab states
const hoveredRelation = ref(null)
const selectedRelationId = ref('art-user') // defaults to artworks -> users

const selectTab = (tab) => {
  activeTab.value = tab
  if (tab !== 'usecases') {
    pauseScenario()
  }
}

// Scenarios definition for Use Cases interactive simulation
const scenarios = [
  {
    id: 'purchase',
    name: 'Achat d\'œuvre d\'art (Purchase Flow)',
    actor: 'collector',
    color: '#eab308', // gold
    steps: [
      {
        title: '1. Action Utilisateur (Front)',
        desc: 'Le collectionneur clique sur "Acheter" sur la fiche d\'une œuvre. L\'application client vérifie la connexion et compile les détails de la transaction.',
        code: 'const payload = { artwork_id: "665f9..." };\nconst token = localStorage.getItem("token");\n// Déclenche l\'overlay de chargement sur le bouton...',
        path: 'M 140 100 C 200 100, 230 180, 290 180',
        activeNodes: ['collector', 'client']
      },
      {
        title: '2. Requête API REST (Réseau)',
        desc: 'Le client Vue envoie une requête HTTP POST sécurisée à l\'API FastAPI avec le jeton Bearer dans les en-têtes.',
        code: 'POST http://localhost:8000/orders\nAuthorization: Bearer <JWT_TOKEN>\nContent-Type: application/json\n\n{ "artwork_id": "665f9..." }',
        path: 'M 410 200 C 440 200, 460 200, 490 200',
        activeNodes: ['client', 'backend']
      },
      {
        title: '3. Persistance & Transactions (BDD)',
        desc: 'FastAPI décode le jeton, marque l\'œuvre d\'art comme vendue (is_sold = true) pour la verrouiller, et insère l\'achat dans MongoDB.',
        code: 'db.artworks.updateOne({ _id: ObjectId("665f9...") }, { $set: { is_sold: true } });\ndb.orders.insertOne({ user_id: "usr_...", artwork_id: "art_...", price: 1200 });',
        path: 'M 610 200 C 640 200, 660 200, 690 200',
        activeNodes: ['backend', 'database']
      },
      {
        title: '4. Retour de Confirmation (Front)',
        desc: 'Le serveur répond avec 201 Created. L\'application Web met à jour le panier, libère le verrou d\'achat et affiche le succès.',
        code: 'HTTP/1.1 201 Created\nContent-Type: application/json\n\n{ "id": "ord_7812", "status": "confirmed", "price": 1200 }',
        path: 'M 490 220 C 460 220, 440 220, 410 220',
        activeNodes: ['backend', 'client']
      }
    ]
  },
  {
    id: 'publish',
    name: 'Publication d\'œuvre (Publish Flow)',
    actor: 'artist',
    color: '#3b82f6', // blue
    steps: [
      {
        title: '1. Saisie Formulaire (Front)',
        desc: 'L\'artiste remplit le formulaire de création (titre, prix, catégorie, URL de l\'image) dans son studio.',
        code: 'const newArtwork = {\n  title: "Le Bassin aux Nymphéas",\n  price: 3200,\n  category: "Peinture",\n  image_url: "https://..."\n};',
        path: 'M 140 200 C 200 200, 230 200, 290 200',
        activeNodes: ['artist', 'client']
      },
      {
        title: '2. Contrôle d\'Autorisations (Réseau)',
        desc: 'L\'API FastAPI reçoit l\'œuvre. Elle décode le token Bearer pour extraire l\'identité de l\'artiste et vérifier son rôle.',
        code: 'POST http://localhost:8000/artworks\nAuthorization: Bearer <JWT_TOKEN>\nBody: { "title": "Le Bassin aux Nymphéas", ... }',
        path: 'M 410 200 C 440 200, 460 200, 490 200',
        activeNodes: ['client', 'backend']
      },
      {
        title: '3. Enregistrement MongoDB (BDD)',
        desc: 'FastAPI insère le document avec les champs author_id et author_name de l\'artiste connecté.',
        code: 'db.artworks.insertOne({\n  title: "Le Bassin aux Nymphéas",\n  author_id: "usr_artist_99",\n  author_name: "Claude Monet",\n  is_sold: false\n})',
        path: 'M 610 200 C 640 200, 660 200, 690 200',
        activeNodes: ['backend', 'database']
      },
      {
        title: '4. Galerie actualisée (Front)',
        desc: 'La BDD renvoie l\'ID créé. FastAPI répond à l\'UI Vue 3. L\'application recharge les catalogues d\'art en temps réel.',
        code: 'HTTP/1.1 201 Created\nContent-Type: application/json\n\n{ "_id": "art_28931", "title": "Le Bassin aux Nymphéas", ... }',
        path: 'M 490 220 C 460 220, 440 220, 410 220',
        activeNodes: ['backend', 'client']
      }
    ]
  },
  {
    id: 'admin',
    name: 'Gestion Administrative (Admin Flow)',
    actor: 'admin',
    color: '#a855f7', // purple
    steps: [
      {
        title: '1. Saisie de Catégorie (Front)',
        desc: 'L\'administrateur saisit une nouvelle catégorie (ex: "Sculpture") dans son panneau d\'administration.',
        code: 'const catData = { name: "Sculpture" };',
        path: 'M 140 300 C 200 300, 230 220, 290 220',
        activeNodes: ['admin', 'client']
      },
      {
        title: '2. Validation du Rôle Admin (Réseau)',
        desc: 'La requête est transmise. Le middleware FastAPI décode le token JWT et vérifie que le rôle est "admin".',
        code: 'POST http://localhost:8000/categories\nAuthorization: Bearer <JWT_TOKEN>\nBody: { "name": "Sculpture" }',
        path: 'M 410 200 C 440 200, 460 200, 490 200',
        activeNodes: ['client', 'backend']
      },
      {
        title: '3. Enregistrement sous Contrainte (BDD)',
        desc: 'MongoDB insère la nouvelle catégorie sous réserve d\'unicité de l\'index sur le nom.',
        code: 'db.categories.insertOne({ name: "Sculpture" });\n// Renvoie une exception si déjà existante (index unique)',
        path: 'M 610 200 C 640 200, 660 200, 690 200',
        activeNodes: ['backend', 'database']
      },
      {
        title: '4. Propagation Système (Front)',
        desc: 'Le client web met à jour la liste globale des filtres et actualise la navigation de tous les catalogues.',
        code: 'HTTP/1.1 201 Created\nState updated: categories = ["Peinture", "Digital", "Sculpture"]',
        path: 'M 490 220 C 460 220, 440 220, 410 220',
        activeNodes: ['backend', 'client']
      }
    ]
  }
]

const activeScenario = computed(() => {
  return scenarios.find(s => s.id === activeScenarioId.value)
})

const activeStep = computed(() => {
  return activeScenario.value.steps[currentStepIndex.value]
})

const selectScenario = (id) => {
  pauseScenario()
  activeScenarioId.value = id
  currentStepIndex.value = 0
}

const nextStep = () => {
  if (currentStepIndex.value < activeScenario.value.steps.length - 1) {
    currentStepIndex.value++
  } else {
    currentStepIndex.value = 0
  }
}

const prevStep = () => {
  if (currentStepIndex.value > 0) {
    currentStepIndex.value--
  } else {
    currentStepIndex.value = activeScenario.value.steps.length - 1
  }
}

const togglePlay = () => {
  if (isPlaying.value) {
    pauseScenario()
  } else {
    isPlaying.value = true
    playInterval = setInterval(() => {
      nextStep()
    }, 4000)
  }
}

const pauseScenario = () => {
  isPlaying.value = false
  if (playInterval) {
    clearInterval(playInterval)
    playInterval = null
  }
}

const resetScenario = () => {
  pauseScenario()
  currentStepIndex.value = 0
}

onBeforeUnmount(() => {
  pauseScenario()
})

// Database relations details
const dbRelations = {
  'art-user': {
    title: 'artworks ➔ users (Champ: author_id)',
    type: 'Many-to-One (N:1)',
    desc: 'Associe chaque œuvre d\'art à l\'artiste créateur. Le champ author_id de la collection artworks stocke l\'identifiant _id (sous forme de chaîne) de la collection users.',
    code: `# Pipeline FastAPI + Motor pour récupérer l\'œuvre avec son artiste\npipeline = [\n    {\n        "$lookup": {\n            "from": "users",\n            "localField": "author_id",\n            "foreignField": "_id",\n            "as": "artist"\n        }\n    },\n    { "$unwind": "$artist" }\n]\nresults = await db.artworks.aggregate(pipeline).to_list(100)`
  },
  'art-cat': {
    title: 'artworks ➔ categories (Champ: category)',
    type: 'Many-to-One (N:1)',
    desc: 'Associe une œuvre à sa catégorie thématique. Le champ category stocke le nom textuel unique (ex: "Peinture") qui est indexé de manière unique dans la collection categories.',
    code: `# Validation de l\'existence de la catégorie lors de la création d\'une œuvre\ncat = await db.categories.find_one({"name": new_artwork.category})\nif not cat:\n    raise HTTPException(status_code=400, detail="Catégorie inexistante")`
  },
  'ord-user': {
    title: 'orders ➔ users (Champ: user_id)',
    type: 'Many-to-One (N:1)',
    desc: 'Liaison de commande pour identifier l\'acheteur. Le champ user_id de la collection orders contient l\'identifiant unique _id du collectionneur.',
    code: `# Récupère les commandes passées par un utilisateur spécifique\norders = await db.orders.find({"user_id": current_user.id}).to_list(100)`
  },
  'ord-art': {
    title: 'orders ➔ artworks (Champ: artwork_id)',
    type: 'One-to-One (1:1) Unique',
    desc: 'Indique l\'œuvre achetée lors de la transaction. L\'unicité de la relation est maintenue logiquement car une œuvre vendue (is_sold: true) ne peut plus faire l\'objet d\'une nouvelle commande.',
    code: `# Pipeline d\'agrégation pour inspecter le détail de l\'œuvre achetée\npipeline = [\n    {\n        "$lookup": {\n            "from": "artworks",\n            "localField": "artwork_id",\n            "foreignField": "_id",\n            "as": "artwork_details"\n        }\n    },\n    { "$unwind": "$artwork_details" }\n]\norder_details = await db.orders.aggregate(pipeline).to_list(100)`
  }
}

const activeRelation = computed(() => {
  return dbRelations[selectedRelationId.value]
})

const selectRelation = (relId) => {
  selectedRelationId.value = relId
}

// Compute table highlighting based on relation selection
const isTableRelated = (tableName) => {
  const rel = selectedRelationId.value
  if (rel === 'art-user') return tableName === 'artworks' || tableName === 'users'
  if (rel === 'art-cat') return tableName === 'artworks' || tableName === 'categories'
  if (rel === 'ord-user') return tableName === 'orders' || tableName === 'users'
  if (rel === 'ord-art') return tableName === 'orders' || tableName === 'artworks'
  return false
}
</script>

<template>
  <div style="padding: 1rem 0 4rem;" class="animate-fade-in">
    <!-- Header -->
    <div style="text-align: center; margin-bottom: 3rem;">
      <span style="font-size: 0.85rem; font-weight: 600; color: var(--accent-color); text-transform: uppercase; letter-spacing: 0.1em; display: inline-flex; align-items: center; gap: 0.5rem;">
        <Layers size="14" /> Architecture Board
      </span>
      <h1 style="font-size: clamp(2.5rem, 5vw, 3.5rem); font-weight: 500; margin: 0.5rem 0 1rem;">Conception & Documentation</h1>
      <p style="font-size: 1.1rem; opacity: 0.7; max-width: 600px; margin: 0 auto; font-weight: 300;">
        Explorez un plan interactif et hautement animé du système E-Gallery, ses cas d'utilisation et ses relations de données.
      </p>
    </div>

    <!-- Tab navigation -->
    <div class="glass-panel" style="display: flex; gap: 0.5rem; padding: 0.5rem; border-radius: var(--radius-md); margin-bottom: 3rem; overflow-x: auto; scrollbar-width: none;">
      <button 
        @click="selectTab('architecture')" 
        class="btn" 
        :class="activeTab === 'architecture' ? 'btn-primary' : 'btn-secondary'"
        style="flex: 1; min-width: 160px; justify-content: center; padding: 0.75rem 1rem;"
      >
        <Cpu size="16" /> Architecture Globale
      </button>
      <button 
        @click="selectTab('usecases')" 
        class="btn" 
        :class="activeTab === 'usecases' ? 'btn-primary' : 'btn-secondary'"
        style="flex: 1; min-width: 160px; justify-content: center; padding: 0.75rem 1rem;"
      >
        <RefreshCw size="16" /> Cas d'Utilisation
      </button>
      <button 
        @click="selectTab('components')" 
        class="btn" 
        :class="activeTab === 'components' ? 'btn-primary' : 'btn-secondary'"
        style="flex: 1; min-width: 160px; justify-content: center; padding: 0.75rem 1rem;"
      >
        <Layers size="16" /> Arborescence Vue
      </button>
      <button 
        @click="selectTab('database')" 
        class="btn" 
        :class="activeTab === 'database' ? 'btn-primary' : 'btn-secondary'"
        style="flex: 1; min-width: 160px; justify-content: center; padding: 0.75rem 1rem;"
      >
        <Database size="16" /> Schéma Relationnel
      </button>
      <button 
        @click="selectTab('styleguide')" 
        class="btn" 
        :class="activeTab === 'styleguide' ? 'btn-primary' : 'btn-secondary'"
        style="flex: 1; min-width: 160px; justify-content: center; padding: 0.75rem 1rem;"
      >
        <Palette size="16" /> Guide Graphique
      </button>
    </div>

    <!-- Active Tab Content -->
    <div class="glass-panel" style="padding: 3rem; border-radius: var(--radius-lg); min-height: 480px; position: relative; overflow: hidden;">
      
      <!-- 1. Technical Architecture -->
      <div v-if="activeTab === 'architecture'" class="animate-fade-in">
        <h2 style="font-size: 1.8rem; font-weight: 500; margin-bottom: 2rem; display: flex; align-items: center; gap: 0.5rem;">
          <Cpu style="color: var(--accent-color);" /> Architecture Technique & Flux de Données
        </h2>
        <p style="opacity: 0.8; margin-bottom: 3rem; max-width: 700px;">
          E-Gallery implémente une architecture découplée. L'application cliente communique en asynchrone via des routes REST vers un serveur FastAPI, lequel persiste l'état dans MongoDB.
        </p>

        <!-- Animated SVG Pipeline Diagram -->
        <div style="position: relative; padding: 2rem 0; width: 100%; display: flex; justify-content: center; align-items: center; background: rgba(0,0,0,0.1); border-radius: var(--radius-md); border: 1px solid var(--border-color); overflow-x: auto;">
          <svg width="800" height="200" viewBox="0 0 800 200" style="display: block; min-width: 800px;">
            <!-- Connection Lines -->
            <path d="M 170 100 L 330 100" stroke="var(--border-color)" stroke-width="2" />
            <path d="M 470 100 L 630 100" stroke="var(--border-color)" stroke-width="2" />
            
            <!-- Animated Signal Pulses -->
            <circle r="4" fill="var(--accent-color)">
              <animateMotion dur="4s" repeatCount="indefinite" path="M 170 100 L 330 100" />
            </circle>
            <circle r="4" fill="#3b82f6">
              <animateMotion dur="4s" begin="2s" repeatCount="indefinite" path="M 330 100 L 170 100" />
            </circle>
            <circle r="4" fill="var(--accent-color)">
              <animateMotion dur="3s" repeatCount="indefinite" path="M 470 100 L 630 100" />
            </circle>
            <circle r="4" fill="#3b82f6">
              <animateMotion dur="3s" begin="1.5s" repeatCount="indefinite" path="M 630 100 L 470 100" />
            </circle>

            <!-- Node 1: Client Application -->
            <g transform="translate(50, 50)" style="cursor: pointer;" @mouseenter="hoveredNode = 'client'" @mouseleave="hoveredNode = null">
              <rect x="0" y="0" width="120" height="100" rx="12" fill="var(--card-bg)" stroke="var(--border-color)" stroke-width="1.5" />
              <rect v-if="hoveredNode === 'client'" x="0" y="0" width="120" height="100" rx="12" fill="none" stroke="var(--accent-color)" stroke-width="2" class="pulse-outline" />
              <foreignObject x="10" y="15" width="100" height="70">
                <div style="text-align: center; color: var(--text-color); display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; gap: 0.35rem;">
                  <Smartphone size="20" style="color: var(--accent-color);" />
                  <span style="font-weight: 600; font-size: 0.85rem;">Client Web</span>
                  <span style="font-size: 0.65rem; opacity: 0.6;">Vue 3 + Vite</span>
                </div>
              </foreignObject>
            </g>

            <!-- Node 2: REST API Backend -->
            <g transform="translate(330, 50)" style="cursor: pointer;" @mouseenter="hoveredNode = 'backend'" @mouseleave="hoveredNode = null">
              <rect x="0" y="0" width="140" height="100" rx="12" fill="var(--card-bg)" stroke="var(--border-color)" stroke-width="1.5" />
              <rect v-if="hoveredNode === 'backend'" x="0" y="0" width="140" height="100" rx="12" fill="none" stroke="var(--accent-color)" stroke-width="2" class="pulse-outline" />
              <foreignObject x="10" y="15" width="120" height="70">
                <div style="text-align: center; color: var(--text-color); display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; gap: 0.35rem;">
                  <Server size="20" style="color: var(--accent-color);" />
                  <span style="font-weight: 600; font-size: 0.85rem;">Serveur API REST</span>
                  <span style="font-size: 0.65rem; opacity: 0.6;">FastAPI + Uvicorn</span>
                </div>
              </foreignObject>
            </g>

            <!-- Node 3: Database -->
            <g transform="translate(630, 50)" style="cursor: pointer;" @mouseenter="hoveredNode = 'database'" @mouseleave="hoveredNode = null">
              <rect x="0" y="0" width="120" height="100" rx="12" fill="var(--card-bg)" stroke="var(--border-color)" stroke-width="1.5" />
              <rect v-if="hoveredNode === 'database'" x="0" y="0" width="120" height="100" rx="12" fill="none" stroke="var(--accent-color)" stroke-width="2" class="pulse-outline" />
              <foreignObject x="10" y="15" width="100" height="70">
                <div style="text-align: center; color: var(--text-color); display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; gap: 0.35rem;">
                  <Database size="20" style="color: var(--accent-color);" />
                  <span style="font-weight: 600; font-size: 0.85rem;">Base de Données</span>
                  <span style="font-size: 0.65rem; opacity: 0.6;">MongoDB</span>
                </div>
              </foreignObject>
            </g>
          </svg>
        </div>

        <!-- Node description drawer -->
        <div style="margin-top: 2rem;">
          <transition name="slide-fade" mode="out-in">
            <div v-if="hoveredNode === 'client'" :key="'c'" class="glass-panel" style="padding: 1.5rem; background: var(--secondary-bg);">
              <h4 style="font-weight: 600; margin-bottom: 0.5rem; color: var(--accent-color);">Frontend (Vue 3 + Vite)</h4>
              <p style="font-size: 0.9rem; opacity: 0.85; line-height: 1.6;">
                L'interface utilisateur s'appuie sur un routage dynamique (`vue-router`) et un gestionnaire d'état Pinia. Les requêtes réseau sont gérées de manière asynchrone, propageant le token Bearer JWT stocké localement.
              </p>
            </div>
            <div v-else-if="hoveredNode === 'backend'" :key="'b'" class="glass-panel" style="padding: 1.5rem; background: var(--secondary-bg);">
              <h4 style="font-weight: 600; margin-bottom: 0.5rem; color: var(--accent-color);">Serveur API REST (FastAPI)</h4>
              <p style="font-size: 0.9rem; opacity: 0.85; line-height: 1.6;">
                Fournit des endpoints performants, valide les charges utiles (schemas Pydantic), gère la sécurité (hachage direct Bcrypt & génération de tokens JWT) et orchestre les flux transactionnels.
              </p>
            </div>
            <div v-else-if="hoveredNode === 'database'" :key="'d'" class="glass-panel" style="padding: 1.5rem; background: var(--secondary-bg);">
              <h4 style="font-weight: 600; margin-bottom: 0.5rem; color: var(--accent-color);">Base de données (MongoDB)</h4>
              <p style="font-size: 0.9rem; opacity: 0.85; line-height: 1.6;">
                Persiste les utilisateurs, les catégories de galeries, les transactions d'achats et les fiches d'œuvres. Utilise des index pour optimiser la vitesse de recherche.
              </p>
            </div>
            <div v-else :key="'e'" style="padding: 1.5rem; border: 1px dashed var(--border-color); border-radius: var(--radius-md); text-align: center; opacity: 0.5; font-size: 0.9rem;">
              Survolez un nœud du diagramme ci-dessus pour inspecter ses caractéristiques techniques.
            </div>
          </transition>
        </div>
      </div>

      <!-- 2. Use Cases Flow -->
      <div v-if="activeTab === 'usecases'" class="animate-fade-in">
        <h2 style="font-size: 1.8rem; font-weight: 500; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
          <RefreshCw style="color: var(--accent-color);" /> Simulateur de Cas d'Utilisation Interactif
        </h2>
        <p style="opacity: 0.8; margin-bottom: 2.5rem; max-width: 700px;">
          Visualisez le trajet exact emprunté par les données lors d'interactions clés. Sélectionnez un scénario et utilisez le lecteur interactif pour suivre le flux.
        </p>

        <!-- Use Cases Interactive Diagram Canvas -->
        <div style="width: 100%; display: flex; justify-content: center; background: rgba(0,0,0,0.15); padding: 2rem 0; border-radius: var(--radius-md); border: 1px solid var(--border-color); position: relative; overflow-x: auto;">
          <svg width="800" height="380" viewBox="0 0 800 380" style="display: block; min-width: 800px;">
            <defs>
              <linearGradient id="yellowGlow" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#fef08a" />
                <stop offset="100%" stop-color="#eab308" />
              </linearGradient>
              <linearGradient id="blueGlow" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#93c5fd" />
                <stop offset="100%" stop-color="#3b82f6" />
              </linearGradient>
              <linearGradient id="purpleGlow" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#f3e8ff" />
                <stop offset="100%" stop-color="#a855f7" />
              </linearGradient>
            </defs>

            <!-- Background connections paths (Inactive state) -->
            <path d="M 140 100 C 200 100, 230 180, 290 180" fill="none" stroke="var(--border-color)" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.4" />
            <path d="M 140 200 C 200 200, 230 200, 290 200" fill="none" stroke="var(--border-color)" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.4" />
            <path d="M 140 300 C 200 300, 230 220, 290 220" fill="none" stroke="var(--border-color)" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.4" />
            <path d="M 410 200 C 440 200, 460 200, 490 200" fill="none" stroke="var(--border-color)" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.4" />
            <path d="M 610 200 C 640 200, 660 200, 690 200" fill="none" stroke="var(--border-color)" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.4" />
            <path d="M 490 220 C 460 220, 440 220, 410 220" fill="none" stroke="var(--border-color)" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.4" />

            <!-- Active Connection highlight -->
            <path 
              :d="activeStep.path" 
              fill="none" 
              :stroke="activeScenario.color" 
              stroke-width="3.5" 
              stroke-linecap="round"
              style="transition: stroke 0.3s, d 0.3s;"
            />

            <!-- Running Signal Pulse -->
            <circle r="6" :fill="activeScenario.color" :key="activeScenarioId + '-' + currentStepIndex" style="filter: drop-shadow(0 0 4px var(--accent-color));">
              <animateMotion :path="activeStep.path" dur="2s" repeatCount="indefinite" />
            </circle>

            <!-- 1. ACTORS (Left column) -->
            <!-- Collector -->
            <g transform="translate(20, 60)" style="cursor: pointer;" @click="selectScenario('purchase')">
              <rect x="0" y="0" width="120" height="70" rx="10" fill="var(--card-bg)" :stroke="activeStep.activeNodes.includes('collector') ? '#eab308' : 'var(--border-color)'" :stroke-width="activeStep.activeNodes.includes('collector') ? 2.5 : 1.5" style="transition: stroke 0.3s, stroke-width 0.3s;" />
              <foreignObject x="5" y="10" width="110" height="50">
                <div style="text-align: center; color: var(--text-color); display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; gap: 0.15rem;">
                  <User size="16" style="color: #eab308;" />
                  <span style="font-weight: 600; font-size: 0.8rem;">Collectionneur</span>
                  <span style="font-size: 0.6rem; opacity: 0.6;">Achat d'art</span>
                </div>
              </foreignObject>
            </g>

            <!-- Artist -->
            <g transform="translate(20, 160)" style="cursor: pointer;" @click="selectScenario('publish')">
              <rect x="0" y="0" width="120" height="70" rx="10" fill="var(--card-bg)" :stroke="activeStep.activeNodes.includes('artist') ? '#3b82f6' : 'var(--border-color)'" :stroke-width="activeStep.activeNodes.includes('artist') ? 2.5 : 1.5" style="transition: stroke 0.3s, stroke-width 0.3s;" />
              <foreignObject x="5" y="10" width="110" height="50">
                <div style="text-align: center; color: var(--text-color); display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; gap: 0.15rem;">
                  <Smartphone size="16" style="color: #3b82f6;" />
                  <span style="font-weight: 600; font-size: 0.8rem;">Artiste Créateur</span>
                  <span style="font-size: 0.6rem; opacity: 0.6;">Publication d'art</span>
                </div>
              </foreignObject>
            </g>

            <!-- Admin -->
            <g transform="translate(20, 260)" style="cursor: pointer;" @click="selectScenario('admin')">
              <rect x="0" y="0" width="120" height="70" rx="10" fill="var(--card-bg)" :stroke="activeStep.activeNodes.includes('admin') ? '#a855f7' : 'var(--border-color)'" :stroke-width="activeStep.activeNodes.includes('admin') ? 2.5 : 1.5" style="transition: stroke 0.3s, stroke-width 0.3s;" />
              <foreignObject x="5" y="10" width="110" height="50">
                <div style="text-align: center; color: var(--text-color); display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; gap: 0.15rem;">
                  <Shield size="16" style="color: #a855f7;" />
                  <span style="font-weight: 600; font-size: 0.8rem;">Administrateur</span>
                  <span style="font-size: 0.6rem; opacity: 0.6;">Modération</span>
                </div>
              </foreignObject>
            </g>

            <!-- 2. CLIENT WEB (Middle-Left) -->
            <g transform="translate(290, 150)">
              <rect x="0" y="0" width="120" height="100" rx="12" fill="var(--card-bg)" :stroke="activeStep.activeNodes.includes('client') ? activeScenario.color : 'var(--border-color)'" :stroke-width="activeStep.activeNodes.includes('client') ? 2.5 : 1.5" style="transition: stroke 0.3s, stroke-width 0.3s;" />
              <foreignObject x="5" y="10" width="110" height="80">
                <div style="text-align: center; color: var(--text-color); display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; gap: 0.25rem;">
                  <Smartphone size="18" style="color: var(--accent-color);" />
                  <span style="font-weight: 600; font-size: 0.85rem;">Client Vue 3</span>
                  <span style="font-size: 0.65rem; opacity: 0.6;">E-Gallery App</span>
                </div>
              </foreignObject>
            </g>

            <!-- 3. FASTAPI BACKEND (Middle-Right) -->
            <g transform="translate(490, 150)">
              <rect x="0" y="0" width="120" height="100" rx="12" fill="var(--card-bg)" :stroke="activeStep.activeNodes.includes('backend') ? activeScenario.color : 'var(--border-color)'" :stroke-width="activeStep.activeNodes.includes('backend') ? 2.5 : 1.5" style="transition: stroke 0.3s, stroke-width 0.3s;" />
              <foreignObject x="5" y="10" width="110" height="80">
                <div style="text-align: center; color: var(--text-color); display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; gap: 0.25rem;">
                  <Server size="18" style="color: var(--accent-color);" />
                  <span style="font-weight: 600; font-size: 0.85rem;">API REST</span>
                  <span style="font-size: 0.65rem; opacity: 0.6;">FastAPI Engine</span>
                </div>
              </foreignObject>
            </g>

            <!-- 4. MONGO DATABASE (Right) -->
            <g transform="translate(690, 150)">
              <rect x="0" y="0" width="100" height="100" rx="12" fill="var(--card-bg)" :stroke="activeStep.activeNodes.includes('database') ? activeScenario.color : 'var(--border-color)'" :stroke-width="activeStep.activeNodes.includes('database') ? 2.5 : 1.5" style="transition: stroke 0.3s, stroke-width 0.3s;" />
              <foreignObject x="5" y="10" width="90" height="80">
                <div style="text-align: center; color: var(--text-color); display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; gap: 0.25rem;">
                  <Database size="18" style="color: var(--accent-color);" />
                  <span style="font-weight: 600; font-size: 0.85rem;">MongoDB</span>
                  <span style="font-size: 0.65rem; opacity: 0.6;">Persistance</span>
                </div>
              </foreignObject>
            </g>
          </svg>
        </div>

        <!-- Simulation Player Controls Panel -->
        <div class="glass-panel" style="padding: 1.5rem; margin-top: 1.5rem; display: flex; flex-direction: column; gap: 1.5rem; border: 1px solid var(--border-color);">
          
          <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem;">
            <!-- Player control triggers -->
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <button @click="prevStep" class="btn btn-secondary" style="padding: 0.5rem 0.75rem;" title="Étape précédente">
                <ChevronLeft size="16" />
              </button>
              <button @click="togglePlay" class="btn btn-primary" style="padding: 0.5rem 1.25rem; display: flex; align-items: center; gap: 0.5rem; min-width: 120px; justify-content: center;">
                <component :is="isPlaying ? Pause : Play" size="16" />
                <span>{{ isPlaying ? 'Pause' : 'Simuler' }}</span>
              </button>
              <button @click="nextStep" class="btn btn-secondary" style="padding: 0.5rem 0.75rem;" title="Étape suivante">
                <ChevronRight size="16" />
              </button>
              <button @click="resetScenario" class="btn btn-secondary" style="padding: 0.5rem 0.75rem;" title="Réinitialiser">
                <RotateCcw size="16" />
              </button>
            </div>

            <!-- Flow selector toggles -->
            <div style="display: flex; gap: 0.35rem; background: rgba(0,0,0,0.2); padding: 0.25rem; border-radius: var(--radius-sm);">
              <button 
                v-for="s in scenarios" 
                :key="s.id"
                @click="selectScenario(s.id)"
                class="btn"
                :style="{
                  padding: '0.45rem 0.9rem',
                  fontSize: '0.75rem',
                  border: 'none',
                  background: activeScenarioId === s.id ? s.color : 'transparent',
                  color: activeScenarioId === s.id ? '#0a0a0a' : 'var(--text-color)',
                  fontWeight: activeScenarioId === s.id ? '600' : '400'
                }"
              >
                {{ s.id === 'purchase' ? 'Achat' : s.id === 'publish' ? 'Publication' : 'Admin' }}
              </button>
            </div>

            <!-- Step indicator -->
            <div style="font-size: 0.85rem; font-weight: 500; opacity: 0.85;">
              Étape <span :style="{ color: activeScenario.color, fontWeight: '600' }">{{ currentStepIndex + 1 }}</span> / {{ activeScenario.steps.length }}
            </div>
          </div>

          <!-- Step Details Description & Code Payload -->
          <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 2rem; align-items: start; flex-wrap: wrap;">
            <div>
              <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; opacity: 0.5; letter-spacing: 0.05em; display: inline-block; margin-bottom: 0.25rem;" :style="{ color: activeScenario.color }">
                Flux actif • {{ activeScenario.name }}
              </span>
              <h4 style="font-weight: 600; margin-bottom: 0.75rem; font-size: 1.15rem; color: var(--text-color);">
                {{ activeStep.title }}
              </h4>
              <p style="font-size: 0.9rem; opacity: 0.85; line-height: 1.6; margin: 0;">
                {{ activeStep.desc }}
              </p>
            </div>

            <div style="background: rgba(0,0,0,0.3); border-radius: var(--radius-sm); border: 1px solid var(--border-color); padding: 1rem; position: relative;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem;">
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; opacity: 0.4; letter-spacing: 0.05em; display: flex; align-items: center; gap: 0.25rem;">
                  <Code size="10" /> Charge utile / Opération
                </span>
                <span style="font-size: 0.65rem; padding: 0.15rem 0.35rem; border-radius: 4px; background: rgba(255, 255, 255, 0.08); color: var(--accent-color); font-weight: 600; font-family: monospace;">
                  JSON / NoSQL
                </span>
              </div>
              <pre style="margin: 0; font-family: monospace; font-size: 0.75rem; color: #a3e635; overflow-x: auto; white-space: pre-wrap; word-break: break-all; max-height: 140px; line-height: 1.45;">{{ activeStep.code }}</pre>
            </div>
          </div>

        </div>
      </div>

      <!-- 3. Component Tree -->
      <div v-if="activeTab === 'components'" class="animate-fade-in" style="text-align: left;">
        <h2 style="font-size: 1.8rem; font-weight: 500; margin-bottom: 2rem; display: flex; align-items: center; gap: 0.5rem;">
          <Layers style="color: var(--accent-color);" /> Arborescence des Composants Vue 3
        </h2>
        <p style="opacity: 0.8; margin-bottom: 2.5rem; max-width: 700px;">
          La structure du front-end s'organise autour de routes d'affichage principales et d'un store global. Survolez les fichiers pour en savoir plus.
        </p>

        <!-- Dynamic component directory visualizer -->
        <div style="display: grid; grid-template-columns: 1fr 1.2fr; gap: 3rem; align-items: start;">
          <div style="background: rgba(0,0,0,0.15); border: 1px solid var(--border-color); padding: 1.5rem; border-radius: var(--radius-md); font-family: monospace; font-size: 0.9rem;">
            <div style="padding-left: 0rem; margin-bottom: 0.5rem;">📂 src/</div>
            <div style="padding-left: 1.5rem; margin-bottom: 0.5rem; cursor: pointer; color: var(--accent-color); font-weight: 600;" @mouseenter="hoveredNode = 'appVue'">
              📄 App.vue
            </div>
            <div style="padding-left: 1.5rem; margin-bottom: 0.5rem;">📁 views/</div>
            <div style="padding-left: 3rem; margin-bottom: 0.5rem; cursor: pointer; color: var(--accent-color);" @mouseenter="hoveredNode = 'homeVue'">
              📄 Home.vue
            </div>
            <div style="padding-left: 3rem; margin-bottom: 0.5rem; cursor: pointer; color: var(--accent-color);" @mouseenter="hoveredNode = 'artVue'">
              📄 Artwork.vue
            </div>
            <div style="padding-left: 3rem; margin-bottom: 0.5rem; cursor: pointer; color: var(--accent-color);" @mouseenter="hoveredNode = 'loginVue'">
              📄 Login.vue
            </div>
            <div style="padding-left: 3rem; margin-bottom: 0.5rem; cursor: pointer; color: var(--accent-color);" @mouseenter="hoveredNode = 'artistVue'">
              📄 DashboardArtist.vue
            </div>
            <div style="padding-left: 3rem; margin-bottom: 0.5rem; cursor: pointer; color: var(--accent-color);" @mouseenter="hoveredNode = 'adminVue'">
              📄 DashboardAdmin.vue
            </div>
            <div style="padding-left: 1.5rem; margin-bottom: 0.5rem;">📁 store/</div>
            <div style="padding-left: 3rem; cursor: pointer; color: var(--accent-color);" @mouseenter="hoveredNode = 'storeAuth'">
              📄 auth.js (Pinia Store)
            </div>
          </div>

          <!-- Description Box -->
          <div class="glass-panel" style="padding: 2rem; min-height: 240px; background: var(--secondary-bg);">
            <transition name="slide-fade" mode="out-in">
              <div v-if="hoveredNode === 'appVue'" :key="'1'">
                <h4 style="font-weight: 600; color: var(--accent-color); margin-bottom: 0.5rem;">App.vue (Conteneur Racine)</h4>
                <p style="font-size: 0.85rem; opacity: 0.8; line-height: 1.6;">
                  Gère le squelette applicatif global : barre de navigation à floutage de fond, pied de page et zone principale. Assure la persistance des sessions en appelant `/auth/me` à l'initialisation et gère l'état linguistique globale (FR/EN).
                </p>
              </div>
              <div v-else-if="hoveredNode === 'homeVue'" :key="'2'">
                <h4 style="font-weight: 600; color: var(--accent-color); margin-bottom: 0.5rem;">Home.vue (Galerie de Découverte)</h4>
                <p style="font-size: 0.85rem; opacity: 0.8; line-height: 1.6;">
                  Point d'entrée de la galerie d'art. Propose les filtres par catégories de créations, la recherche par mots-clés, et le tri par date et par prix. Utilise des transitions d'entrée asynchrones pour l'affichage des œuvres.
                </p>
              </div>
              <div v-else-if="hoveredNode === 'artVue'" :key="'3'">
                <h4 style="font-weight: 600; color: var(--accent-color); margin-bottom: 0.5rem;">Artwork.vue (Détail de l'Œuvre)</h4>
                <p style="font-size: 0.85rem; opacity: 0.8; line-height: 1.6;">
                  Affiche en grand format une œuvre unique. Connecté à la route d'achat POST `/orders`, il propose un flux sécurisé avec écrans de chargement et des messages de confirmation dynamique d'acquisition.
                </p>
              </div>
              <div v-else-if="hoveredNode === 'loginVue'" :key="'4'">
                <h4 style="font-weight: 600; color: var(--accent-color); margin-bottom: 0.5rem;">Login.vue (Portail d'Accès)</h4>
                <p style="font-size: 0.85rem; opacity: 0.8; line-height: 1.6;">
                  Formulaire d'authentification et d'inscription avec transitions fluides entre les onglets. Permet aux nouveaux utilisateurs de sélectionner leur profil (Collectionneur ou Artiste) et affiche des alertes de validation.
                </p>
              </div>
              <div v-else-if="hoveredNode === 'artistVue'" :key="'5'">
                <h4 style="font-weight: 600; color: var(--accent-color); margin-bottom: 0.5rem;">DashboardArtist.vue (Studio Artiste)</h4>
                <p style="font-size: 0.85rem; opacity: 0.8; line-height: 1.6;">
                  Espace personnel des créateurs. Regroupe les statistiques financières (ventes totales, œuvres vendues) ainsi qu'un outil de téléversement et de mise en vente d'art avec attribution automatique d'auteur.
                </p>
              </div>
              <div v-else-if="hoveredNode === 'adminVue'" :key="'6'">
                <h4 style="font-weight: 600; color: var(--accent-color); margin-bottom: 0.5rem;">DashboardAdmin.vue (Panneau Admin)</h4>
                <p style="font-size: 0.85rem; opacity: 0.8; line-height: 1.6;">
                  Console d'administration générale. Permet la gestion des utilisateurs inscrits et de configurer dynamiquement de nouvelles catégories d'art disponibles sur la plateforme.
                </p>
              </div>
              <div v-else-if="hoveredNode === 'storeAuth'" :key="'7'">
                <h4 style="font-weight: 600; color: var(--accent-color); margin-bottom: 0.5rem;">auth.js (Store Pinia)</h4>
                <p style="font-size: 0.85rem; opacity: 0.8; line-height: 1.6;">
                  Gère la session de l'utilisateur : stockage persistant des identifiants et des droits d'accès. Synchronise l'en-tête d'autorisation Bearer de manière globale sur toutes les requêtes Axios.
                </p>
              </div>
              <div v-else :key="'8'">
                <h4 style="font-weight: 600; opacity: 0.6; margin-bottom: 0.5rem;">Détails du composant</h4>
                <p style="font-size: 0.85rem; opacity: 0.5;">Survolez l'arborescence des fichiers à gauche pour voir la description.</p>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- 4. MongoDB Schema -->
      <div v-if="activeTab === 'database'" class="animate-fade-in">
        <h2 style="font-size: 1.8rem; font-weight: 500; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
          <Database style="color: var(--accent-color);" /> Schéma Relationnel & Clés de Liaison
        </h2>
        <p style="opacity: 0.8; margin-bottom: 2.5rem; max-width: 700px;">
          Explorez les relations de données entre les collections MongoDB. Cliquez sur une relation (ligne de couleur ou clé 🔗 FK) pour charger la documentation de jointure et le code d'agrégation.
        </p>

        <!-- Dynamic Database Relational Diagram Canvas -->
        <div style="width: 100%; display: flex; justify-content: center; background: rgba(0,0,0,0.15); padding: 2rem 0; border-radius: var(--radius-md); border: 1px solid var(--border-color); position: relative; overflow-x: auto;">
          <svg width="800" height="460" viewBox="0 0 800 460" style="display: block; min-width: 800px;">
            
            <!-- Relations Connectors (Bezier Curves) -->
            <!-- 1. artworks.author_id -> users._id (Artworks and Users) -->
            <path 
              d="M 490 115 C 400 115, 400 90, 310 90" 
              fill="none" 
              :stroke="selectedRelationId === 'art-user' || hoveredRelation === 'art-user' ? '#3b82f6' : 'var(--border-color)'" 
              :stroke-width="selectedRelationId === 'art-user' || hoveredRelation === 'art-user' ? 3.5 : 1.5"
              style="transition: stroke 0.3s, stroke-width 0.3s;"
            />
            <circle v-if="selectedRelationId === 'art-user' || hoveredRelation === 'art-user'" r="4.5" fill="#3b82f6">
              <animateMotion path="M 490 115 C 400 115, 400 90, 310 90" dur="2s" repeatCount="indefinite" />
            </circle>

            <!-- 2. artworks.category -> categories.name -->
            <path 
              d="M 490 140 C 370 140, 430 355, 310 355" 
              fill="none" 
              :stroke="selectedRelationId === 'art-cat' || hoveredRelation === 'art-cat' ? '#ec4899' : 'var(--border-color)'" 
              :stroke-width="selectedRelationId === 'art-cat' || hoveredRelation === 'art-cat' ? 3.5 : 1.5"
              style="transition: stroke 0.3s, stroke-width 0.3s;"
            />
            <circle v-if="selectedRelationId === 'art-cat' || hoveredRelation === 'art-cat'" r="4.5" fill="#ec4899">
              <animateMotion path="M 490 140 C 370 140, 430 355, 310 355" dur="2s" repeatCount="indefinite" />
            </circle>

            <!-- 3. orders.user_id -> users._id -->
            <path 
              d="M 490 355 C 370 355, 430 90, 310 90" 
              fill="none" 
              :stroke="selectedRelationId === 'ord-user' || hoveredRelation === 'ord-user' ? '#a855f7' : 'var(--border-color)'" 
              :stroke-width="selectedRelationId === 'ord-user' || hoveredRelation === 'ord-user' ? 3.5 : 1.5"
              style="transition: stroke 0.3s, stroke-width 0.3s;"
            />
            <circle v-if="selectedRelationId === 'ord-user' || hoveredRelation === 'ord-user'" r="4.5" fill="#a855f7">
              <animateMotion path="M 490 355 C 370 355, 430 90, 310 90" dur="2s" repeatCount="indefinite" />
            </circle>

            <!-- 4. orders.artwork_id -> artworks._id -->
            <path 
              d="M 750 380 C 820 380, 820 90, 750 90" 
              fill="none" 
              :stroke="selectedRelationId === 'ord-art' || hoveredRelation === 'ord-art' ? '#22c55e' : 'var(--border-color)'" 
              :stroke-width="selectedRelationId === 'ord-art' || hoveredRelation === 'ord-art' ? 3.5 : 1.5"
              style="transition: stroke 0.3s, stroke-width 0.3s;"
            />
            <circle v-if="selectedRelationId === 'ord-art' || hoveredRelation === 'ord-art'" r="4.5" fill="#22c55e">
              <animateMotion path="M 750 380 C 820 380, 820 90, 750 90" dur="2s" repeatCount="indefinite" />
            </circle>


            <!-- Invisible thick paths to capture hovers easily (UX) -->
            <path d="M 490 115 C 400 115, 400 90, 310 90" fill="none" stroke="transparent" stroke-width="15" style="cursor: pointer;" @click="selectRelation('art-user')" @mouseenter="hoveredRelation = 'art-user'" @mouseleave="hoveredRelation = null" />
            <path d="M 490 140 C 370 140, 430 355, 310 355" fill="none" stroke="transparent" stroke-width="15" style="cursor: pointer;" @click="selectRelation('art-cat')" @mouseenter="hoveredRelation = 'art-cat'" @mouseleave="hoveredRelation = null" />
            <path d="M 490 355 C 370 355, 430 90, 310 90" fill="none" stroke="transparent" stroke-width="15" style="cursor: pointer;" @click="selectRelation('ord-user')" @mouseenter="hoveredRelation = 'ord-user'" @mouseleave="hoveredRelation = null" />
            <path d="M 750 380 C 820 380, 820 90, 750 90" fill="none" stroke="transparent" stroke-width="15" style="cursor: pointer;" @click="selectRelation('ord-art')" @mouseenter="hoveredRelation = 'ord-art'" @mouseleave="hoveredRelation = null" />


            <!-- Collection Cards Groups -->
            <!-- 1. users Table (Top-Left) -->
            <g transform="translate(50, 30)" :opacity="isTableRelated('users') ? 1.0 : 0.45" style="transition: opacity 0.3s;">
              <!-- Container Card -->
              <rect x="0" y="0" width="260" height="150" rx="8" fill="#141414" :stroke="selectedRelationId === 'art-user' || selectedRelationId === 'ord-user' ? '#3b82f6' : '#262626'" stroke-width="1.5" />
              <!-- Table Header -->
              <rect x="0" y="0" width="260" height="35" rx="8" fill="#1e293b" />
              <rect x="0" y="30" width="260" height="5" fill="#1e293b" />
              <text x="15" y="22" fill="#94a3b8" font-size="12" font-weight="700" font-family="monospace">📋 users</text>
              <!-- Fields -->
              <g transform="translate(15, 50)" font-family="monospace" font-size="11">
                <!-- _id Row -->
                <text x="0" y="15" fill="#eab308" font-weight="600">🔑 _id</text>
                <text x="230" y="15" fill="#64748b" text-anchor="end">ObjectId [PK]</text>
                <!-- email Row -->
                <text x="0" y="40" fill="#f5f5f4">email</text>
                <text x="230" y="40" fill="#64748b" text-anchor="end">String</text>
                <!-- username Row -->
                <text x="0" y="65" fill="#f5f5f4">username</text>
                <text x="230" y="65" fill="#64748b" text-anchor="end">String</text>
                <!-- role Row -->
                <text x="0" y="90" fill="#f5f5f4">role</text>
                <text x="230" y="90" fill="#64748b" text-anchor="end">String</text>
              </g>
            </g>

            <!-- 2. categories Table (Bottom-Left) -->
            <g transform="translate(50, 270)" :opacity="isTableRelated('categories') ? 1.0 : 0.45" style="transition: opacity 0.3s;">
              <!-- Container Card -->
              <rect x="0" y="0" width="260" height="120" rx="8" fill="#141414" :stroke="selectedRelationId === 'art-cat' ? '#ec4899' : '#262626'" stroke-width="1.5" />
              <!-- Table Header -->
              <rect x="0" y="0" width="260" height="35" rx="8" fill="#4d0e2e" />
              <rect x="0" y="30" width="260" height="5" fill="#4d0e2e" />
              <text x="15" y="22" fill="#f472b6" font-size="12" font-weight="700" font-family="monospace">📋 categories</text>
              <!-- Fields -->
              <g transform="translate(15, 50)" font-family="monospace" font-size="11">
                <!-- _id Row -->
                <text x="0" y="15" fill="#eab308" font-weight="600">🔑 _id</text>
                <text x="230" y="15" fill="#64748b" text-anchor="end">ObjectId [PK]</text>
                <!-- name Row -->
                <text x="0" y="40" fill="#ec4899" font-weight="600" style="cursor: pointer;" @click="selectRelation('art-cat')">🔑 name</text>
                <text x="230" y="40" fill="#64748b" text-anchor="end">String [UQ]</text>
              </g>
            </g>

            <!-- 3. artworks Table (Top-Right) -->
            <g transform="translate(490, 30)" :opacity="isTableRelated('artworks') ? 1.0 : 0.45" style="transition: opacity 0.3s;">
              <!-- Container Card -->
              <rect x="0" y="0" width="260" height="200" rx="8" fill="#141414" :stroke="selectedRelationId === 'art-user' || selectedRelationId === 'art-cat' || selectedRelationId === 'ord-art' ? '#eab308' : '#262626'" stroke-width="1.5" />
              <!-- Table Header -->
              <rect x="0" y="0" width="260" height="35" rx="8" fill="#422006" />
              <rect x="0" y="30" width="260" height="5" fill="#422006" />
              <text x="15" y="22" fill="#fef08a" font-size="12" font-weight="700" font-family="monospace">📋 artworks</text>
              <!-- Fields -->
              <g transform="translate(15, 50)" font-family="monospace" font-size="11">
                <!-- _id Row -->
                <text x="0" y="15" fill="#eab308" font-weight="600" style="cursor: pointer;" @click="selectRelation('ord-art')">🔑 _id</text>
                <text x="230" y="15" fill="#64748b" text-anchor="end">ObjectId [PK]</text>
                
                <!-- author_id Row -->
                <text x="0" y="40" fill="#3b82f6" font-weight="600" style="cursor: pointer;" @click="selectRelation('art-user')" @mouseenter="hoveredRelation = 'art-user'" @mouseleave="hoveredRelation = null">🔗 author_id</text>
                <text x="230" y="40" fill="#64748b" text-anchor="end">String [FK]</text>
                
                <!-- category Row -->
                <text x="0" y="65" fill="#ec4899" font-weight="600" style="cursor: pointer;" @click="selectRelation('art-cat')" @mouseenter="hoveredRelation = 'art-cat'" @mouseleave="hoveredRelation = null">🔗 category</text>
                <text x="230" y="65" fill="#64748b" text-anchor="end">String [FK]</text>
                
                <!-- title Row -->
                <text x="0" y="90" fill="#f5f5f4">title</text>
                <text x="230" y="90" fill="#64748b" text-anchor="end">String</text>
                
                <!-- price Row -->
                <text x="0" y="115" fill="#f5f5f4">price</text>
                <text x="230" y="115" fill="#64748b" text-anchor="end">Double</text>
                
                <!-- is_sold Row -->
                <text x="0" y="140" fill="#22c55e">is_sold</text>
                <text x="230" y="140" fill="#64748b" text-anchor="end">Boolean</text>
              </g>
            </g>

            <!-- 4. orders Table (Bottom-Right) -->
            <g transform="translate(490, 270)" :opacity="isTableRelated('orders') ? 1.0 : 0.45" style="transition: opacity 0.3s;">
              <!-- Container Card -->
              <rect x="0" y="0" width="260" height="160" rx="8" fill="#141414" :stroke="selectedRelationId === 'ord-user' || selectedRelationId === 'ord-art' ? '#22c55e' : '#262626'" stroke-width="1.5" />
              <!-- Table Header -->
              <rect x="0" y="0" width="260" height="35" rx="8" fill="#064e3b" />
              <rect x="0" y="30" width="260" height="5" fill="#064e3b" />
              <text x="15" y="22" fill="#a7f3d0" font-size="12" font-weight="700" font-family="monospace">📋 orders</text>
              <!-- Fields -->
              <g transform="translate(15, 50)" font-family="monospace" font-size="11">
                <!-- _id Row -->
                <text x="0" y="15" fill="#eab308" font-weight="600">🔑 _id</text>
                <text x="230" y="15" fill="#64748b" text-anchor="end">ObjectId [PK]</text>
                
                <!-- user_id Row -->
                <text x="0" y="40" fill="#a855f7" font-weight="600" style="cursor: pointer;" @click="selectRelation('ord-user')" @mouseenter="hoveredRelation = 'ord-user'" @mouseleave="hoveredRelation = null">🔗 user_id</text>
                <text x="230" y="40" fill="#64748b" text-anchor="end">String [FK]</text>
                
                <!-- artwork_id Row -->
                <text x="0" y="65" fill="#22c55e" font-weight="600" style="cursor: pointer;" @click="selectRelation('ord-art')" @mouseenter="hoveredRelation = 'ord-art'" @mouseleave="hoveredRelation = null">🔗 artwork_id</text>
                <text x="230" y="65" fill="#64748b" text-anchor="end">String [FK]</text>
                
                <!-- price Row -->
                <text x="0" y="90" fill="#f5f5f4">price</text>
                <text x="230" y="90" fill="#64748b" text-anchor="end">Double</text>
              </g>
            </g>
          </svg>
        </div>

        <!-- Relational aggregation viewer panel -->
        <div class="glass-panel" style="padding: 1.5rem; margin-top: 1.5rem; border: 1px solid var(--border-color); display: grid; grid-template-columns: 1fr 1.2fr; gap: 2rem; align-items: start; flex-wrap: wrap;">
          <div>
            <span style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; opacity: 0.5; color: var(--accent-color); letter-spacing: 0.05em; display: inline-block; margin-bottom: 0.25rem;">
              Relation Active • {{ activeRelation.type }}
            </span>
            <h4 style="font-weight: 600; margin: 0 0 0.75rem 0; font-size: 1.15rem; color: var(--text-color);">
              {{ activeRelation.title }}
            </h4>
            <p style="font-size: 0.88rem; opacity: 0.85; line-height: 1.6; margin: 0;">
              {{ activeRelation.desc }}
            </p>
          </div>

          <div style="background: rgba(0,0,0,0.3); border-radius: var(--radius-sm); border: 1px solid var(--border-color); padding: 1.5rem; position: relative;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem;">
              <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; opacity: 0.4; letter-spacing: 0.05em; display: flex; align-items: center; gap: 0.25rem;">
                <Code size="10" /> Code de Jointure / Pipeline
              </span>
              <span style="font-size: 0.65rem; padding: 0.15rem 0.35rem; border-radius: 4px; background: rgba(59, 130, 246, 0.15); color: #3b82f6; font-weight: 600; font-family: monospace;">
                FastAPI / MongoDB
              </span>
            </div>
            <pre style="margin: 0; font-family: monospace; font-size: 0.75rem; color: #38bdf8; overflow-x: auto; white-space: pre-wrap; line-height: 1.45;">{{ activeRelation.code }}</pre>
          </div>
        </div>

      </div>

      <!-- 5. UI Style Guide -->
      <div v-if="activeTab === 'styleguide'" class="animate-fade-in">
        <h2 style="font-size: 1.8rem; font-weight: 500; margin-bottom: 2rem; display: flex; align-items: center; gap: 0.5rem;">
          <Palette style="color: var(--accent-color);" /> Charte Graphique & Design Tokens
        </h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 3rem;">
          
          <!-- Typography tokens -->
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 500; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Typographie de la Marque</h3>
            
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
              <div class="glass-panel" style="padding: 1.5rem;">
                <span style="font-size: 0.7rem; font-weight: 600; opacity: 0.5; text-transform: uppercase;">Famille de Titre</span>
                <h4 style="font-family: 'Bodoni Moda', serif; font-size: 1.8rem; font-weight: 500; margin-top: 0.25rem;">Bodoni Moda</h4>
                <p style="font-size: 0.8rem; opacity: 0.7; margin-top: 0.5rem; line-height: 1.5;">
                  Un empattement (serif) éditorial haut de gamme, utilisé pour la signature de marque, les grands titres descriptifs et les prix d'art.
                </p>
              </div>
              
              <div class="glass-panel" style="padding: 1.5rem;">
                <span style="font-size: 0.7rem; font-weight: 600; opacity: 0.5; text-transform: uppercase;">Famille de Labeurs</span>
                <h4 style="font-family: 'Jost', sans-serif; font-size: 1.5rem; font-weight: 400; margin-top: 0.25rem;">Jost</h4>
                <p style="font-size: 0.8rem; opacity: 0.7; margin-top: 0.5rem; line-height: 1.5;">
                  Un sans-serif géométrique minimaliste, garantissant une lisibilité optimale sur les formulaires, filtres et tableaux de bord de gestion.
                </p>
              </div>
            </div>
          </div>

          <!-- Color Tokens -->
          <div>
            <h3 style="font-size: 1.25rem; font-weight: 500; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Nuanciers Couleurs</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
              <div class="glass-panel" style="padding: 1rem; text-align: center;">
                <div style="background: #eab308; height: 50px; border-radius: var(--radius-sm); border: 1px solid rgba(255,255,255,0.1); margin-bottom: 0.5rem;"></div>
                <span style="font-size: 0.8rem; font-weight: 600;">Gold Accent</span>
                <p style="font-size: 0.7rem; opacity: 0.6; margin-top: 0.15rem;">#eab308</p>
              </div>

              <div class="glass-panel" style="padding: 1rem; text-align: center;">
                <div style="background: #0a0a0a; height: 50px; border-radius: var(--radius-sm); border: 1px solid rgba(255,255,255,0.1); margin-bottom: 0.5rem;"></div>
                <span style="font-size: 0.8rem; font-weight: 600;">Obsidian Black</span>
                <p style="font-size: 0.7rem; opacity: 0.6; margin-top: 0.15rem;">#0a0a0a</p>
              </div>

              <div class="glass-panel" style="padding: 1rem; text-align: center;">
                <div style="background: #fafaf9; height: 50px; border-radius: var(--radius-sm); border: 1px solid rgba(0,0,0,0.15); margin-bottom: 0.5rem;"></div>
                <span style="color: #000; font-size: 0.8rem; font-weight: 600;">Canvas White</span>
                <p style="color: #000; font-size: 0.7rem; opacity: 0.6; margin-top: 0.15rem;">#fafaf9</p>
              </div>

              <div class="glass-panel" style="padding: 1rem; text-align: center;">
                <div style="background: #262626; height: 50px; border-radius: var(--radius-sm); border: 1px solid rgba(255,255,255,0.1); margin-bottom: 0.5rem;"></div>
                <span style="font-size: 0.8rem; font-weight: 600;">Muted borders</span>
                <p style="font-size: 0.7rem; opacity: 0.6; margin-top: 0.15rem;">#262626</p>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* Keyframe pulse outline animation for hovered SVG nodes */
.pulse-outline {
  animation: pulseStroke 2s infinite ease-in-out;
}

@keyframes pulseStroke {
  0% { stroke-opacity: 0.4; stroke-dasharray: 0 0; }
  50% { stroke-opacity: 1; stroke-dasharray: 6 3; }
  100% { stroke-opacity: 0.4; stroke-dasharray: 0 0; }
}

.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>

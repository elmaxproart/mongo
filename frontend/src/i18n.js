import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    nav: {
      home: 'Home',
      login: 'Login',
      logout: 'Logout',
      gallery: 'Gallery',
      artist: 'Artist Space',
      admin: 'Admin',
      docs: 'Docs'
    },
    hero: {
      title: 'E-Gallery',
      subtitle: 'Discover and collect unique digital art'
    },
    artwork: {
      buy: 'Buy Now',
      author: 'By',
      date: 'Created on',
      category: 'Category'
    },
    auth: {
      login_title: 'Sign In',
      register_title: 'Create Account',
      email: 'Email',
      password: 'Password',
      role: 'Role'
    }
  },
  fr: {
    nav: {
      home: 'Accueil',
      login: 'Connexion',
      logout: 'Déconnexion',
      gallery: 'Galerie',
      artist: 'Espace Artiste',
      admin: 'Admin',
      docs: 'Docs'
    },
    hero: {
      title: 'E-Gallery',
      subtitle: 'Découvrez et collectionnez des œuvres d\'art uniques'
    },
    artwork: {
      buy: 'Acheter',
      author: 'Par',
      date: 'Créé le',
      category: 'Catégorie'
    },
    auth: {
      login_title: 'Se Connecter',
      register_title: 'Créer un Compte',
      email: 'Email',
      password: 'Mot de passe',
      role: 'Rôle'
    }
  }
}

const i18n = createI18n({
  legacy: false,
  locale: 'fr',
  fallbackLocale: 'en',
  messages
})

export default i18n

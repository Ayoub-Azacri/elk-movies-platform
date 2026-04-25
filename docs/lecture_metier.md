# Lecture métier des résultats — Dashboard Kibana

[[kibana_export.ndjson]] | [[demo_script.md]] | [[data_dictionary.md]]

Six visualisations constituent le dashboard "Movies Analytics Dashboard". Pour chacune, une lecture des résultats du point de vue métier (industrie cinématographique).

---

## 1. Pie — Films by genre

**Données** : Drama 25.99%, Documentary 17.06%, Comedy 16.2%, Thriller 8.4%, Action 7.1%

La prédominance du Drame et du Documentaire (43 % cumulés) s'explique par des coûts de production structurellement plus bas que le cinéma de genre. Ces catégories facilitent une production à fort volume, notamment indépendante.

---

## 2. Line — Films per year

**Données** : croissance lente jusqu'aux années 1990, explosion post-2000, léger repli sur les années les plus récentes (données incomplètes pour les titres récents dans le dataset)

L'explosion post-2000 témoigne de la transition vers le numérique et de la multiplication des plateformes de diffusion mondiale, qui ont radicalement réduit les barrières à l'entrée pour les nouveaux producteurs.

---

## 3. Bar — Average budget by genre

**Données** : Adventure ~$8M (plus haut), suivi de Action et Animation. Drama proche de la médiane. Documentary le plus bas.

L'investissement massif dans l'Aventure et l'Action confirme une industrie de blockbusters où le capital se concentre sur les prouesses technologiques. Le Drame reste le standard du récit à coût maîtrisé : volume élevé, budget contenu.

---

## 4. Histogram — Rating distribution

**Données** : `vote_average` concentré entre 6 et 7, distribution légèrement asymétrique à gauche, très peu de films au-dessus de 8

Le marché est saturé de contenus jugés "moyens". Les films notés au-dessus de 8 sont des exceptions statistiques rares — des ancres de prestige pour les studios plutôt que la norme.

---

## 5. Bar — Top 10 films by popularity

**Données** : scores TMDB entre 2 000 et 4 000, écart large entre rang 1 et rang 10, dominance de films post-2000

L'écart entre le premier rang et les suivants illustre une économie de l'attention ultra-polarisée : une poignée de franchises modernes capte l'essentiel de la visibilité culturelle mondiale.

---

## 6. Pie — Films by original language

**Données** : Anglais 51.53%, Français 6.32%, Espagnol 5.72%, autres < 5% chacun

L'anglais confirme son hégémonie commerciale, mais le français et l'espagnol représentent 12 % cumulés — signe de la résilience et du rayonnement international des cinématographies latines face à l'industrie anglo-américaine.

from pathlib import Path
import json, shutil

root = Path(__file__).resolve().parent.parent
site = root / '_site'
photos = json.loads((root / 'photos-2026/manifest.json').read_text())
shutil.copytree(root / 'photos-2026', site / 'photos-2026', dirs_exist_ok=True)
cards = []
for i, p in enumerate(photos):
    name = p['file']
    cards.append(f'<a class="photo2026-card" href="./photos-2026/{name}" data-photo="{i}" aria-label="Agrandir la photo {i+1}"{ " hidden" if i >= 24 else ""}><img src="./photos-2026/thumbs/{name}" alt="Course du Bois Barrat, édition 2026 — photo {i+1}" loading="lazy" width="480" height="320"><span>{i+1:03}</span></a>')
gallery = '''
<style>
#photos-2026{max-width:1200px;margin:3rem auto;padding:2rem 1.25rem;scroll-margin-top:90px}
#photos-2026 .photo2026-heading{text-align:center;margin-bottom:2rem}
#photos-2026 h2{font-size:clamp(1.9rem,5vw,3rem);margin:.4rem 0}
#photos-2026 .photo2026-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
#photos-2026 .photo2026-card{position:relative;display:block;overflow:hidden;border-radius:12px;background:#e5e7df;aspect-ratio:3/2}
#photos-2026 .photo2026-card[hidden]{display:none}
#photos-2026 .photo2026-card img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .2s}
#photos-2026 .photo2026-card:hover img{transform:scale(1.04)}
#photos-2026 .photo2026-card span{position:absolute;bottom:6px;right:8px;background:#142f25b8;color:white;padding:2px 7px;border-radius:5px;font-size:12px}
#photos-2026 button,.photo2026-jump{display:inline-block;background:#284b3c;color:white;border:0;border-radius:30px;padding:14px 24px;cursor:pointer;font:inherit;text-decoration:none}
.photo2026-jump{position:relative;margin:1rem auto;text-align:center}
#photos-2026 .photo2026-more{text-align:center;margin:1.7rem 0}
#photo2026-dialog{border:0;background:#101814;color:white;padding:12px;width:95vw;max-width:1400px;max-height:96dvh;border-radius:12px}
#photo2026-dialog::backdrop{background:#000d}
#photo2026-dialog .viewer-head{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:0 8px 10px}
#photo2026-dialog button{background:#ffffff22;color:white;border:1px solid #ffffff55;border-radius:8px;cursor:pointer;padding:10px 16px;font:inherit}
#photo2026-dialog img{display:block;max-width:100%;width:auto;height:auto;max-height:72dvh;margin:auto;object-fit:contain}
#photo2026-dialog .viewer-foot{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:12px 0 0}
#photo2026-dialog a{color:white;text-decoration:underline}
@media(max-width:760px){#photos-2026 .photo2026-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}#photo2026-dialog .viewer-foot{flex-wrap:wrap}#photo2026-dialog button{padding:10px}}
</style>
<section id="photos-2026" aria-labelledby="photos2026-title">
<div class="photo2026-heading"><p>LES SOUVENIRS DU 24 OCTOBRE</p><h2 id="photos2026-title">Photos de l’édition 2026</h2><p>Merci à toutes et à tous pour cette belle journée à Montesquieu-Lauragais !</p><p>__COUNT__ photos · Cliquez sur une photo pour l’agrandir.</p><p class="photo2026-credit">Crédit photo : <strong>Magali Cattarelli</strong> — <a href="https://www.instagram.com/magali_du_lauragais/" target="_blank" rel="noopener noreferrer" style="color:inherit;text-decoration:underline">@magali_du_lauragais</a></p></div>
<div class="photo2026-grid">__CARDS__</div>
<div class="photo2026-more"><p id="photos2026-count" aria-live="polite">24 photos sur __COUNT__</p><button id="photos2026-more" type="button">Voir plus de photos</button></div>
<noscript><style>#photos-2026 .photo2026-card[hidden]{display:block}#photos-2026 .photo2026-more{display:none}</style></noscript>
</section>
<dialog id="photo2026-dialog" aria-label="Photo de l’édition 2026">
<div class="viewer-head"><span id="photo2026-position" aria-live="polite"></span><button id="photo2026-close" type="button" autofocus>Fermer ✕</button></div>
<img id="photo2026-image" alt="">
<div class="viewer-foot"><button id="photo2026-prev" type="button" aria-label="Photo précédente">← Précédente</button><a id="photo2026-download" download>Télécharger la photo</a><button id="photo2026-next" type="button" aria-label="Photo suivante">Suivante →</button></div>
</dialog>
<script>
(()=>{
 const cards=[...document.querySelectorAll('.photo2026-card')],dialog=document.getElementById('photo2026-dialog'),image=document.getElementById('photo2026-image');
 let shown=24,index=0,opener=null;
 function show(i){index=(i+cards.length)%cards.length;image.src=cards[index].href;image.alt=cards[index].querySelector('img').alt;document.getElementById('photo2026-position').textContent=`Photo ${index+1} / ${cards.length}`;document.getElementById('photo2026-download').href=image.src;}
 cards.forEach((a,i)=>a.addEventListener('click',e=>{if(!dialog.showModal)return;e.preventDefault();opener=a;show(i);dialog.showModal();}));
 document.getElementById('photos2026-more').addEventListener('click',e=>{shown=Math.min(shown+48,cards.length);cards.slice(0,shown).forEach(a=>a.hidden=false);document.getElementById('photos2026-count').textContent=`${shown} photos sur ${cards.length}`;e.target.hidden=shown===cards.length;});
 document.getElementById('photo2026-close').onclick=()=>dialog.close();
 document.getElementById('photo2026-prev').onclick=()=>show(index-1);
 document.getElementById('photo2026-next').onclick=()=>show(index+1);
 dialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();show(index-1);}if(e.key==='ArrowRight'){e.preventDefault();show(index+1);}});
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
 dialog.addEventListener('close',()=>{image.removeAttribute('src');opener?.focus();});
})();
</script>
'''.replace('__COUNT__', str(len(photos))).replace('__CARDS__', '\n'.join(cards))
path=site/'index.html'
html=path.read_text()
# Place the album before the existing page footer, inside main where available.
if '</main>' in html: html=html.replace('</main>', gallery+'\n</main>', 1)
else: html=html.replace('</body>',gallery+'\n</body>',1)
# Make the album easy to find immediately on arrival.
import re
html=re.sub(r'(<main\b[^>]*>)',r'\1<div style="text-align:center"><a class="photo2026-jump" href="#photos-2026">📷 Voir les photos de l’édition 2026</a></div>',html,count=1)
path.write_text(html)
(site/'404.html').write_text(html)
print(f'Galerie ajoutée : {len(photos)} photos')

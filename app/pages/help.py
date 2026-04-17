"""Help page: short, non-technical intro for new colleagues."""

from nicegui import ui

from app.components.layout import page_layout
from app.config import Settings
from app.wiki import WikiStore

HELP_HTML = """
<h1>Wat is de PKW Wiki?</h1>

<p><strong>In het kort:</strong> een doorzoekbare verzameling van bijna 100 beleidsdocumenten
(WDODelta, Unie van Waterschappen, Rijk, Europa) met per document een korte samenvatting
en verwijzingen naar verwante begrippen. Je vindt in minuten wat anders uren bladeren kost.</p>

<h2>Waarom bestaat deze wiki?</h2>

<p>Als waterschap hebben we te maken met een enorme hoeveelheid beleid: eigen vastgesteld
beleid, richtlijnen van de Unie van Waterschappen, Europese wetgeving (zoals de AI-verordening),
Rijksbeleid, provinciaal beleid, standaarden van HWH en IHW.</p>

<p>Niemand leest al die documenten. Ze staan verspreid over PDF's, websites en SharePoints.
Als je een vraag hebt — <em>"Wat zegt beleid eigenlijk over X?"</em> — moet je vaak door
tientallen documenten heen.</p>

<p>Deze wiki lost dat op. Alle relevante beleidsdocumenten staan op één plek, zijn
doorzoekbaar gemaakt, en zijn met elkaar verbonden via gedeelde begrippen.</p>

<h2>Wat zit erin?</h2>

<p>Op dit moment bijna 100 beleidsdocumenten, waaronder:</p>

<ul>
  <li>Beleid van WDODelta zelf</li>
  <li>Unie van Waterschappen (AI-kompas, handreikingen, meerjarenplannen)</li>
  <li>Rijksoverheid (Algoritmekader, BIO2, generatieve AI-visie)</li>
  <li>Europa (AI Act, AVG, Data Act, NIS2)</li>
  <li>Sectorale standaarden (Aquo, DAMO, Digitale Delta API)</li>
</ul>

<h2>Wat kun je ermee?</h2>

<ol>
  <li><strong>Zoeken op onderwerp</strong> — typ een begrip, zie in welke documenten het voorkomt en wat er precies staat.</li>
  <li><strong>Begrippen opzoeken</strong> — per concept (bijv. "AI-geletterdheid", "federatief datastelsel") een samenvatting met verwijzingen naar de bronnen.</li>
  <li><strong>Bronnen vergelijken</strong> — zien waar beleidsdocumenten elkaar aanvullen of juist tegenspreken.</li>
  <li><strong>Snel de essentie</strong> — elke bron heeft een korte samenvatting, zodat je niet het hele document hoeft te lezen om te weten of het relevant is.</li>
</ol>

<h2>Wanneer gebruik je het?</h2>

<ul>
  <li>Je schrijft een notitie, advies of projectplan en wilt weten wat bestaand beleid hierover zegt.</li>
  <li>Je krijgt een vraag over compliance (AI Act, AVG, BIO2) en wilt snel de relevante passages vinden.</li>
  <li>Je oriënteert je op een nieuw onderwerp en wilt weten welke documenten ertoe doen.</li>
  <li>Je wilt checken of een idee past binnen de bestaande kaders.</li>
</ul>

<h2>Belangrijk om te weten</h2>

<ul>
  <li>De wiki <strong>vervangt de officiële documenten niet</strong> — voor formele besluitvorming gebruik je altijd het originele document.</li>
  <li>De wiki is een <strong>startpunt en navigatie-instrument</strong>, geen juridisch bindende bron.</li>
  <li>Ontbreekt er een document dat jij belangrijk vindt? Laat het weten, dan voeg ik het toe.</li>
</ul>
"""


def register(store: WikiStore, settings: Settings) -> None:

    @ui.page("/help")
    def help_page() -> None:
        with page_layout("Help"):
            with ui.element("div").classes("wiki-content"):
                ui.html(HELP_HTML)

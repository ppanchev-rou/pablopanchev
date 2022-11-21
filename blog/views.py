from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement


# Create your views here.
def animal_list(request):
    animals = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/animal_list.html', {'animals':animals, 'equipements':equipements})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    equipements = Equipement.objects.all()
    lieu = animal.lieu
    if request.method == "POST":
        ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        form = MoveForm(request.POST, instance=animal)
        if form.is_valid():
            form.save(commit=False)
            nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
            if nouveau_lieu.disponibilite=='libre' and nouveau_lieu.id_equip=='mangeoire' and animal.etat == 'affamé':
                animal.etat='repus'
                animal.save()
                ancien_lieu.disponibilite='libre'
                ancien_lieu.save()
                nouveau_lieu.disponibilite='occupé'
                nouveau_lieu.save()
                return redirect('animal_detail', id_animal=id_animal)
            elif nouveau_lieu.disponibilite=='libre' and nouveau_lieu.id_equip=='roue' and animal.etat == 'repus':
                animal.etat='fatigue'
                animal.save()
                ancien_lieu.disponibilite='libre'
                ancien_lieu.save()
                nouveau_lieu.disponibilite='occupé'
                nouveau_lieu.save()
                return redirect('animal_detail', id_animal=id_animal)
            elif nouveau_lieu.disponibilite=='libre' and nouveau_lieu.id_equip=='nid' and animal.etat == 'fatigue':
                animal.etat='endormi'
                animal.save()
                ancien_lieu.disponibilite='libre'
                ancien_lieu.save()
                nouveau_lieu.disponibilite='occupé'
                nouveau_lieu.save()
                return redirect('animal_detail', id_animal=id_animal)
            elif nouveau_lieu.disponibilite=='libre' and nouveau_lieu.id_equip=='litière' and animal.etat == 'endormi':
                animal.etat='affamé'
                animal.save()
                ancien_lieu.disponibilite='libre'
                ancien_lieu.save()
                return redirect('animal_detail', id_animal=id_animal)
            else:
                message="L'animal ne peut pas être déplacé"
                return render(request, 'blog/animal_detail.html', {'animal': animal, 'lieu': lieu, 'form': form, 'message': message})
    else:
        message='Ok !'
        form = MoveForm()
        return render(request,
                  'blog/animal_detail.html',
                  {'animal': animal, 'lieu': lieu, 'form': form, 'message': message, 'equipements':equipements})
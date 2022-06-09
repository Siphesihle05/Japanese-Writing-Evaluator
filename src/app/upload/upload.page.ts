import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { Observable, ReplaySubject } from 'rxjs';
import { AppServiceService } from '../services/app-service.service';
import { CharacterImage, UploadedImage } from '../shared/image';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.page.html',
  styleUrls: ['./upload.page.scss'],
})
export class UploadPage implements OnInit {

  characterImage: CharacterImage;
  uploadedImage: File;
  private score: number;

  //TODO:add form parameters to constructor, #71, Phumu
  constructor(private service: AppServiceService,public alertController: AlertController) { }

  //TODO: get the character image to be practiced, #71, Phumu
  ngOnInit() {
    this.characterImage = this.service.getTryImage();
  }
// ${this.characterImage.url}
  //TODO: show popover when evaluate is clicked, #71, Phumu
  async showScore(score: number) {
    const scoreMessage = 'Your accuracy score is '+ score.toString();
    const alert = await this.alertController.create({
      cssClass: 'my-custom-class',
      header: 'Score',
      message: `<ion-img src="" alt="Uploaded image" width="100" height="100"></ion-img>${scoreMessage}`,
      buttons: [
        {
          text: 'Ok',
          handler: () => {
            console.log('Confirm Okay');
          }
        }
      ]
    });

    await alert.present();

    const { role } = await alert.onDidDismiss();
    console.log('onDidDismiss resolved with role', role);
  }

  //TODO: send image to backend to be evaluated by the AI, #71, Phumu
  evaluateImage() {
    // add if user is a guest
    if (this.uploadedImage != null && localStorage.getItem('id') !== '') {
      let img = new Object() as UploadedImage;
      let base64String = '';
      this.convertImageToBase64(this.uploadedImage).subscribe(data => {
        base64String = data;
      });
      img = {
        userId: localStorage.getItem('id'),
        uploadedImage: base64String,
        characterName: this.characterImage.characterName,
        group: this.characterImage.group,
      };

      if (localStorage.getItem('id') !== 'guest') {
        this.service.uploadImage(img).subscribe( data =>{
          this.score = data.body.score;
        });
        this.showScore(this.score); // get the score
      }
      else{
        this.service.guestUploadImage(img).subscribe( data => {
          this.score = data.body.score;
        });
        this.showScore(this.score);
      }
    }
  }

  //TODO: get uploaded image from the file input, #71, Phumu
  getUploadedImage($event){
    this.uploadedImage = $event.target.files[0];
  }

  convertImageToBase64(file: File): Observable<string>{ // convert the image file to base64
    const base64Result = new ReplaySubject<string>(1);
    const fileReader = new FileReader();
    fileReader.readAsBinaryString(file);
    fileReader.onload = (e)=>{
      base64Result.next(btoa(e.target.result.toString()));
    };
    return base64Result;
  }

}

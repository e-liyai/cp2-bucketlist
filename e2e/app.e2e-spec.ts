import { Cp2AngularBucketlistPage } from './app.po';

describe('cp2-angular-bucketlist App', function() {
  let page: Cp2AngularBucketlistPage;

  beforeEach(() => {
    page = new Cp2AngularBucketlistPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});

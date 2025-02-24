!!! info
This guide was submitted by a community member. Find something wrong? Submit a PR to get it fixed!

In a lot of ways, Home Assistant is why this project exists! Since Cena has a robust API it makes it a great fit for interacting with Home Assistant and pulling information into your dashboard.

### Get Todays Meal in Lovelace

Starting in v0.4.1 you are now able to use the uri `/api​/meal-plans​/today​/image?group_name=Home` to directly access the image to todays meal. This makes it incredibly easy to include the image into your Home Assistant Dashboard using the picture entity.

Here's an example where `sensor.cena_todays_meal` is pulling in the meal-plan name and I'm using the url to get the image.

![api-extras-gif](../../assets/img/home-assistant-card.png)

```yaml
type: picture-entity
entity: sensor.cena_todays_meal
name: Dinner Tonight
show_state: true
show_name: true
image: "http://localhost:9000/api/meal-plans/today/image?group_name=Home"
style:
.: |
  ha-card {
  max-height: 300px !important;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  }
```

The sensor that gets the name of the meal can be achieved using the following REST sensor in Home Assistant

```yaml
sensor:
  - platform: rest
    resource: "http://localhost:9000/api/meal-plans/today"
    method: GET
    name: Cena todays meal
    headers:
      Authorization: Bearer MySuperSecretBearerCode
    value_template: "{{ value_json.name }}"
```

The Bearer token can be created from the User Settings page (https://hay-kot.github.io/cena/documentation/users-groups/user-settings/#api-key-generation)

!!! tip
Due to how Home Assistant works with images, I had to include the additional styling to get the images to not appear distorted. This includes and [additional installation](https://github.com/thomasloven/lovelace-card-mod) from HACS.

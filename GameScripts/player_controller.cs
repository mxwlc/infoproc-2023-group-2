using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class player_controller : MonoBehaviour
{
    // Start is called before the first frame update
    private Transform player;
    public float speed;
    public float maxBound, minBound;
    public float lives = 5;

    public GameObject shot;
    public Transform shotSpawn;
    public float fireRate;

    private float nextFire;

    void Start()
    {
        player = GetComponent<Transform> ();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        float h = Input.GetAxis ("Horizontal");
        if(player.position.x < minBound && h < 0){
            h = 0;
        }
        else if (player.position.x > maxBound && h > 0 ){
            h = 0;
        }
        player.position += Vector3.right * h * speed;
        
    }

    void Update(){
         if (Input.GetKeyDown(KeyCode.Space) && Time.time > nextFire){ //hit space to shoot
            nextFire = Time.time + fireRate; //add time interval for shoot
            Instantiate(shot, shotSpawn.position, shotSpawn.rotation);
        }
        if(lives <=0){
            Destroy (gameObject);
            GameOver.isPlayerDead = true;
        }
    }
}

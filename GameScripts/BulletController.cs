using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BulletController : MonoBehaviour
{
    private Transform bullet;
    public float speed;
    // Start is called before the first frame update
    void Start()
    {
        bullet = GetComponent<Transform> ();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        bullet.position += Vector3.up*speed;
        if(bullet.position.y >= 10){
            Destroy(gameObject);
        }        
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if(other.tag == "Enemy"){
            Destroy (gameObject);
            score.playerScore += 30;
            GameObject Enemy = other.gameObject;
            Destroy (Enemy);
			// InvaderGrid EnemyKilled = Enemy.GetComponent<InvaderGrid> ();
			// EnemyKilled.bodycount += 1; 
        }
        else if (other.tag == "Base"){
            Destroy (gameObject);
        }
    }
}

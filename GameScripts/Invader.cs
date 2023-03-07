using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Invader : MonoBehaviour
{
    public InvaderGrid invaderGrid;
    private Transform invader;
    public System.Action killed;
    // public GameObject EnemyShot;
    // public Transform EnemyShotSpawn;
    // private float EnemyFireRate = 0.995f;
    // private float EnemyNextFire;
    // private bool invaderAttack = false;

    private void Awake()
    {
        invader = GetComponent<Transform>();
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.tag == "Bullet"){
            killed?.Invoke();
            Destroy(gameObject);
            
        }
    }

}

// public GameObject EnemyShot;
    // public Transform EnemyShotSpawn;
    // private float EnemyFireRate = 0.995f;
    // private float EnemyNextFire;
    // private bool invaderAttack = false;

        // // private void Update()
    // // {
    // //     if (invaderAttack && Time.time > EnemyNextFire) {
    // //         EnemyNextFire = Time.time + EnemyFireRate;
    // //         Instantiate(EnemyShot, EnemyShotSpawn.position, EnemyShotSpawn.rotation);
    // //         invaderAttack = false;
    // //     }
    
    // // }

    // public void ActivateShooting() {
    //     invaderAttack = true;
    //     EnemyNextFire = Time.time + 0.1f;
    // }

    // public void DeactivateShooting() {
    //     invaderAttack = false;
    // }
